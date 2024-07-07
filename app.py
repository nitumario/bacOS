from flask import Flask, request, render_template, send_from_directory, jsonify, redirect, url_for, flash, session
import MySQLdb
import os
import json
from datetime import datetime
import uuid



app = Flask(__name__)
app.secret_key = 'test'
db = MySQLdb.connect(host="localhost", user="mario", passwd="toor", db="bacOS")
cursor = db.cursor()
ip = '192.168.56.1'

def datetimeformat(value, format='%Y-%m-%dT%H:%M'):
    if isinstance(value, str):
        dt = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        return dt.strftime(format)
    return value

app.jinja_env.filters['datetimeformat'] = datetimeformat





@app.route('/logout')
def logout():
    session.pop('logged_in', None)  
    flash('You have been logged out', 'success')
    return redirect(url_for('login'))   


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        type = request.form.get('type')
        if type == 'on':
            type = 'asteapta aprobare'
        else:
            type = 'elev'
        user_uuid = uuid.uuid4()
        query = "INSERT INTO users (username, email, password, account_type, UUID) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (username, email, password, type, user_uuid))
        db.commit()
        flash('Account created successfully', 'success')
        

        session['logged_in'] = True
        session['uuid'] = user_uuid
        session['type'] = type
        print("user: ", session['uuid'], "with type: ", session['type'])

        return redirect(url_for('events'))


    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        query = "SELECT * FROM users WHERE email = %s AND password = %s"
        cursor.execute(query, (email, password))
        result = cursor.fetchone()
        
        if result:
            session['logged_in'] = True
            session['uuid'] = result[5]
            session['type'] = result[3]
            print("user: ", session['uuid'], "with type: ", session['type'])
            return redirect(url_for('events'))
        else:
            flash('Invalid credentials', 'error')
            return redirect(url_for('login'))
    return render_template('login.html')
    




@app.route('/creare', methods=['GET', 'POST'])
def creare():
    if 'logged_in' in session and session['logged_in']:

        if request.method == 'POST':
            nume = request.form.get('nume')
            startdatetime = request.form.get('startdatetime')
            durata = request.form.get('durata')
            compiler = request.form.get('compiler')

            if compiler == 'on':
                compiler = True
            else:
                compiler = False

            cursor.execute(f"INSERT INTO events (nume, startdatetime, durata, compiler) VALUES ('{nume}', '{startdatetime}', {durata}, {compiler})")
            db.commit()

            id = str(cursor.lastrowid)
            os.makedirs("events\\" + id)

            subiecte = request.files.getlist('subiecte')
            for file in subiecte:
                if file:
                    file.save(os.path.join("events\\" + id, file.filename))

            test = request.files.get('teste')
            if test:
                test.save(os.path.join(id, test.filename))
        return render_template('creare.html')
    else:
        return redirect(url_for('login'))


@app.route('/api/event/<int:id>', methods=['GET'])
def api_event(id):
    cursor.execute("SELECT * FROM events WHERE id = %s", (id,))
    event = cursor.fetchone()
    if event:
        event_data = {
            'id': event[0],
            'nume': event[1],
            'startdatetime': event[3],
            'durata': event[4],
            'compiler': event[5],
            'subiecte': os.listdir(f"events\\{id}")
        }
        return jsonify(event_data)
    else:
        return jsonify({'error': 'Event not found'}), 404
    

@app.route('/gentest', methods=['GET', 'POST'])
def gentest():
    if 'logged_in' in session and session['logged_in']:
        if request.method == 'POST':
            subiect = request.form.get('subiect')
            input = request.form.get('input')
            id = request.form.get('id_test')
            expected_output = request.form.get('expected_output')
            punctaj = request.form.get('punctaj')

            cursor.execute("SELECT teste FROM events WHERE id = %s", (id,))
            existing_json = cursor.fetchone()[0]

            try:
                existing_data = json.loads(existing_json)
                if not isinstance(existing_data, list):
                    existing_data = []
            except (json.JSONDecodeError, TypeError):
                existing_data = []

            test_data = {
                'id': subiect,
                'input': input,
                'expected_output': expected_output,
                'punctaj': punctaj
            }

            existing_data.append(test_data)

            updated_json = json.dumps(existing_data)

            cursor.execute("UPDATE events SET teste = %s WHERE id = %s", (updated_json, id))
            db.commit()
        
        if request.method == 'GET':
            cursor.execute("SELECT id, nume FROM events")
            events = cursor.fetchall()
            events_with_ids = [{'id': event[0], 'name': event[1]} for event in events]
            return render_template('gentest.html', events_with_ids=events_with_ids)
    else:
        return redirect(url_for('login'))

@app.route('/events', methods=['GET'])
def events():
    cursor.execute("SELECT id, nume FROM events")
    events = cursor.fetchall()
    events_with_ids = [(event[1], event[0]) for event in events]

    return render_template('events.html', events_with_ids=events_with_ids)

@app.route('/event/<id>', methods=['GET', 'POST'])
def event(id):

    cursor.execute("SELECT * FROM events WHERE id = %s", (id,))
    event = cursor.fetchone()
    event_data = {
        'id': event[0],
        'nume': event[1],
        'startdatetime': event[3],
        'durata': event[4],
        'compiler': event[5],
        'subiecte': os.listdir(f"events\\{id}")
    }
    if 'logged_in' in session and session['logged_in'] and session['type'] == 'profesor':
        return render_template('event.html', event_data=event_data)
    else:
        print("meow")
        return render_template('event_uneditable.html', event_data=event_data, readonly=True)






@app.route('/event/<int:id>/edit', methods=['POST'])
def edit_event(id):
    if 'logged_in' in session and session['logged_in']:
        nume = request.form.get('nume')
        startdatetime = request.form.get('startdatetime').replace('T', ' ')
        durata = request.form.get('durata')
        compiler = request.form.get('compiler')
        compiler = True if compiler == 'on' else False

        query = """
            UPDATE events 
            SET nume = %s, startdatetime = %s, durata = %s, compiler = %s 
            WHERE id = %s
        """
        cursor.execute(query, (nume, startdatetime, durata, compiler, id))
        db.commit()

        flash('Event updated successfully', 'success')
        return redirect(url_for('event', id=id))
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(host = ip, port=80, debug=True)

