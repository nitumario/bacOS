from flask import Flask, request, render_template, send_from_directory, jsonify, redirect, url_for, flash, session
import MySQLdb
import os
import json
app = Flask(__name__)
app.secret_key = 'test'
db = MySQLdb.connect(host="localhost", user="mario", passwd="toor", db="bacOS")
cursor = db.cursor()
ip = '192.168.56.1'


@app.route('/creare', methods=['GET', 'POST'])
def creare():
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
                file.save(os.path.join(id, file.filename))

        test = request.files.get('teste')
        if test:
            test.save(os.path.join(id, test.filename))
    return render_template('creare.html')

@app.route('/gentest', methods=['GET', 'POST'])
def gentest():
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

    return render_template('gentest.html')


@app.route('/events', methods=['GET'])
def events():
    cursor.execute("SELECT id, nume FROM events")
    events = cursor.fetchall()
    events_with_ids = [(event[1], event[0]) for event in events]

    return render_template('events.html', events_with_ids=events_with_ids)

@app.route('/event/<id>', methods=['GET'])
def event(id):
    cursor.execute("SELECT * FROM events WHERE id = %s", (id,))
    event = cursor.fetchone()
    event_data = {
        'id': event[0],
        'nume': event[1],
        'startdatetime': event[2],
        'durata': event[3],
        'compiler': event[4],
        'subiecte': os.listdir(f"events\\{id}")
    }

    return render_template('event.html', event_data=event_data)
if __name__ == '__main__':
    app.run(host = ip, port=80, debug=True)