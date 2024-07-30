from flask import Flask, request, render_template, send_from_directory, jsonify, redirect, url_for, flash, session
import MySQLdb
import os
import json
from datetime import datetime
import uuid
import subprocess

ip = '192.168.0.234'
app = Flask(__name__)
app.secret_key = 'test'
db = MySQLdb.connect(host=ip, user="mario", passwd="toor", db="bacOS")
cursor = db.cursor()


def datetimeformat(value, format='%Y-%m-%dT%H:%M'):
    if isinstance(value, str):
        dt = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        return dt.strftime(format)
    return value

app.jinja_env.filters['datetimeformat'] = datetimeformat





@app.route('/upload-api', methods=['POST'])
def upload():
    files = request.files.getlist('files')
    user = request.form.get('user')
    event = request.form.get('event')
    for file in files:
        file_path = os.path.join('rezolvari', user, file.filename)
        if not os.path.isdir(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))
        file.save(file_path)
    subprocess.run('python3 /rezolvari/tests.py ' + event + ' ' + user)

    return ' ', 200





@app.route('/')
def home():
    return redirect(url_for('events'))



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
        print("adding user:", username, email, password, type)
        if type == 'on':
            type = 'asteapta aprobare'
        else:
            type = 'elev'
        user_uuid = uuid.uuid4()
        query = "INSERT INTO users (username, email, password, account_type, UUID) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (username, email, password, type, user_uuid))
        db.commit()
        flash('Account created successfully', 'success')
        
        session['mail'] = email
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
        print(result)
        
        if result:
            session['logged_in'] = True
            session['uuid'] = result[5]
            session['mail'] = email
            session['type'] = result[3]
            print("user: ", session['uuid'], "with type: ", session['type'])
            return redirect(url_for('events'))
        else:
            flash('Invalid credentials', 'error')
            return redirect(url_for('login'))
    return render_template('login.html')
    


@app.route('/creare', methods=['GET', 'POST'])
def creare():
    #modifica doar pt profesori
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

@app.route('/loginapi', methods=['POST'])
def loginapi():
    email = request.form.get('email')
    password = request.form.get('password')

    query = "SELECT * FROM users WHERE email = %s AND password = %s"
    cursor.execute(query, (email, password))
    result = cursor.fetchone()
    
    if result:
        return jsonify({'OK': 'user found'}), 200
    else:
        return jsonify({'error': 'user not found'}), 401

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

@app.route('/subiecte/<int:id>', methods=['GET'])
def subiecte(id):
    return jsonify(os.listdir(f"events\\{id}"))

@app.route('/durata/<int:id>', methods=['GET'])
def durata(id):
    cursor.execute("SELECT durata FROM events WHERE id = %s", (id,))
    durata = cursor.fetchone()
    return jsonify(durata[0])

@app.route('/compiler/<int:id>', methods=['GET'])
def compiler(id):
    cursor.execute("SELECT compiler FROM events WHERE id = %s", (id,))
    compiler = cursor.fetchone()
    return jsonify(compiler[0])


@app.route('/tests/<int:id>', methods=['GET'])
def tests(id):
    cursor.execute("SELECT teste FROM events WHERE id = %s", (id,))
    tests = cursor.fetchone()
    return jsonify(tests[0])

@app.route('/startdatetime/<int:id>', methods=['GET'])
def startdatetime(id):
    cursor.execute("SELECT startdatetime FROM events WHERE id = %s", (id,))
    result = cursor.fetchone()

    # Check if result is not None
    if result:
        startdatetime = result[0]  # This should be a datetime object
        # Format datetime as 'YYYY-MM-DD HH:MM:SS'
        formatted_startdatetime = startdatetime.strftime('%Y-%m-%d %H:%M:%S')
        return jsonify(formatted_startdatetime)

@app.route('/gentest/<int:id>', methods=['GET', 'POST'])
def gentest(id):
    #doar pentru profesori
    if 'logged_in' in session and session['logged_in']:
        if request.method == 'POST':

            subiect = request.form.get('subiect')
            input = request.form.get('input')
            expected_output = request.form.get('expected_output')
            punctaj = request.form.get('punctaj')
            cursor.execute("SELECT teste FROM events WHERE id = %s", (id,))
            existing_json = cursor.fetchone()[0]
            print(id)
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
            return redirect(url_for('event', id=id))

        if request.method == 'GET':

            return render_template('gentest.html', id = id)
    else:
        return redirect(url_for('login'))



@app.route('/events', methods=['GET'])
def events():
    if 'logged_in' in session and session['logged_in']:
        cursor.execute("SELECT username FROM users WHERE UUID = %s", (session['uuid'],))
        user = cursor.fetchone()
        if user:
            username = user[0]
        else:
            username = None

    cursor.execute("SELECT id, nume FROM events")
    events = cursor.fetchall()
    events_with_ids = [(event[1], event[0]) for event in events]

    return render_template('events.html', events_with_ids=events_with_ids )



@app.route('/event/<id>', methods=['GET', 'POST'])
def event(id):
    cursor.execute("SELECT punctaj FROM punctaj WHERE event_id = %s AND username = %s", (id, session['mail']))
    punctaj = cursor.fetchone()
    print(punctaj)


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
    #sa fie pt profesori if ul ca sa fie else ul pt elevi
    if 'logged_in' in session and session['logged_in'] and session['type'] == 'profesor':
        return render_template('event.html', event_data=event_data)
    else:
        return render_template('event_uneditable.html', event_data=event_data, readonly=True, punctaj=punctaj)



@app.route('/event/<int:id>/<path:file_path>')
def download_file(id, file_path):
    directory = os.path.join("events", str(id))
    return send_from_directory(directory, file_path, as_attachment=True)



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
        return redirect(url_for('events'))
    else:
        return redirect(url_for('login'))
    


@app.route('/user/<username>', methods=['GET', 'POST'])
def edit_user(username):
    if 'logged_in' in session and session['logged_in']:
        if request.method == 'POST':
            new_username = request.form.get('username')
            new_email = request.form.get('email')
            new_password = request.form.get('password')
            
            query = """
                UPDATE users 
                SET username = %s, email = %s, password = %s
                WHERE username = %s
            """
            cursor.execute(query, (new_username, new_email, new_password, username))
            db.commit()
            
            flash('User details updated successfully', 'success')
            return redirect(url_for('edit_user', username=new_username))
        
        query = "SELECT username, email, password FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        
        if not user:
            flash('User not found', 'error')
            return redirect(url_for('events'))
        
        user_data = {
            'username': user[0],
            'email': user[1],
            'password': user[2]
        }
        
        return render_template('user.html', user_data=user_data)



@app.route('/despre', methods=['GET'])
def despre():
    return render_template('despre.html')



if __name__ == '__main__':
    app.run(host = ip, port=80, debug=True)
