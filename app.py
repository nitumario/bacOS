from flask import Flask, request, render_template, send_from_directory, jsonify, redirect, url_for, flash, session
from datetime import datetime
import os
import json
from datetime import datetime
import MySQLdb
import subprocess


db = MySQLdb.connect(host="localhost", user="mario", passwd="toor", db="bacOS")
cursor = db.cursor()

app = Flask(__name__)
app.secret_key = 'test'
@app.route('/api', methods=['GET'])
def api():
    event_folders = [folder for folder in os.listdir('.') if folder.startswith('event')]
    event_list = []

    for folder in event_folders:
        event = {}
        event['folder'] = folder
        event['files'] = os.listdir(folder)
        event_list.append(event)


    return jsonify(event_list), 200

links = []

@app.route('/api/rezultate', methods=['POST'])
def rezultate():
    link = request.form.get('link')
    id = request.form.get('id')
    subiect = request.form.get('subiect')
    links.append(link)
    if link == 'done':
        links.pop()
        formatted_links = ' '.join(links)
        print(f"python3 test.py \"{formatted_links}\" {subiect} {id}")
        subprocess.run(f"python3 test.py \"{formatted_links}\" {subiect} {id}")
        links.clear()

    return jsonify({'links': links, 'subiect': subiect, 'id': id }), 200

@app.route('/creare', methods=['GET', 'POST'])
def creare():
    if 'logged_in' not in session or not session['logged_in']:  
        flash('You must be logged in to view this page', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        start_date = request.form.get('start_date')
        start_time = request.form.get('start_time')
        durata = request.form.get('durata')
        compiler = request.form.get('compiler')
        if compiler == 'on':
            compiler = True
        else:
            compiler = False

        date = datetime.strptime(start_date, '%Y-%m-%d')
        time = datetime.strptime(start_time, '%H:%M')
        name = request.form.get('name')
        ziua_start = date.strftime('%d')
        luna_start = date.strftime('%m')
        ora_start = time.strftime('%H')
        minut_start = time.strftime('%M')

        formatted_date = date.strftime('%Y-%m-%d')
        formatted_time = time.strftime('%H:%M')

        directory = f"event_{name}_{ziua_start}{luna_start}{ora_start}{minut_start}"
        os.makedirs(directory, exist_ok=True)
        query = f"CREATE TABLE IF NOT EXISTS {name} (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), punctaj INT CHECK (punctaj >= 0 AND punctaj <= 100))"
        cursor.execute(query)
        db.commit()
        event_data = {
            "name": name,
            "start_date": formatted_date,
            "start_time": formatted_time,
            "durata": durata,
            "compiler": compiler
        }
    
        with open(f"{directory}/event_{name}_{ziua_start}{luna_start}{ora_start}{minut_start}.json", "w") as f:
            json.dump(event_data, f)

        files = request.files.getlist('file1')
        for file in files:
            if file:
                file.save(os.path.join(directory, file.filename))

        teste_files = request.files.getlist('file2')
        file_data_list = []

        for file in teste_files:
            if file:
                file_path = os.path.join(directory, file.filename)
                file.save(file_path)
                with open(file_path, "r") as f:
                    file_data = json.load(f)
                    file_data_list.append(file_data)

        query = "INSERT INTO subiecte (nume, teste) VALUES (%s, %s)"
        values = (name, json.dumps(file_data_list))
        cursor.execute(query, values)
        db.commit()

        for file in teste_files:
            if file:
                os.remove(os.path.join(directory, file.filename))
    return render_template('creare.html')

@app.route('/events', methods=['GET'])
def events():
    if 'logged_in' not in session or not session['logged_in']:  
        flash('You must be logged in to view this page', 'error')
        return redirect(url_for('login'))

    event_folders = [folder for folder in os.listdir('.') if folder.startswith('event')]
    files_by_folder = {}
    print(session.get('username'))
    punctaj = None
    for folder in event_folders:
        folder_name = folder.split("_")[1]
        files = [file for file in os.listdir(folder) if not file.endswith('.json')]
        user = session.get('username')
        query = f"SELECT punctaj FROM {folder_name} WHERE username = %s"
        cursor.execute(query, (user,))
        result = cursor.fetchone()

        punctaj = "Nu ai participat la aceasta competitie" if not result else result[0]
        files_by_folder[folder_name] = files
        print(punctaj)

    return render_template('events.html', files_by_folder=files_by_folder,punctaj=punctaj)



@app.route('/events/<event_folder>', methods=['GET'])
def see_contents(event_folder):
    full_path = os.path.join('.', event_folder)
    files = os.listdir(full_path)
    
    return render_template('event.html', files=files, event_folder=event_folder)




@app.route('/events/<event_folder>/<file>', methods=['GET'])
def download_file(event_folder, file):
    
    folder_datetime = event_folder[-8:]
    current_datetime = datetime.now()
    current_datetime = current_datetime.strftime('%d%m%H%M')
    current_datetime = datetime.strptime(current_datetime, '%d%m%H%M')

    folder_datetime = datetime.strptime(folder_datetime, '%d%m%H%M')

    time_difference = (current_datetime - folder_datetime).total_seconds() / 60

    if time_difference < 0:
        hours = int(-time_difference) // 60
        minutes = int(-time_difference) % 60
        return (f"Acest eveniment incepe in {hours} ore si {minutes} minute", 423)
    elif time_difference > 100000:
        return 'Acest eveniment s-a terminat', 423
    else:
        return send_from_directory(event_folder, file)


@app.route('/', methods=['GET'])
def home():
    if 'logged_in' in session and session['logged_in']:
        return render_template('index.html')
    return redirect(url_for('login'))

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
            session['email'] = email
            session['username'] = result[1]
            return redirect(url_for('events'))
        else:
            flash('Invalid credentials', 'error')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
        try:
            cursor.execute(query, (username, email, password))
            db.commit()
            flash('Account created successfully', 'success')
            
 
            session['logged_in'] = True
            return redirect(url_for('events'))
        except db.connector.Error as err:
            flash('Error: {}'.format(err), 'error')
            return redirect(url_for('register'))

    return render_template('login.html')

@app.route('/punctaje', methods=['GET'])
def punctaje():
    query = "SELECT * FROM users"
    cursor.execute(query)
    subiecte = cursor.fetchall()
    return render_template('punctaje.html', subiecte=subiecte)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)  
    flash('You have been logged out', 'success')
    return redirect(url_for('login'))
 
if __name__ == '__main__':
    app.run(host = '192.168.1.7', port=80, debug=True)
