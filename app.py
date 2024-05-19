from flask import Flask, request, render_template, send_from_directory, jsonify, redirect, url_for, flash, session
from datetime import datetime
import os
import json
from datetime import datetime
import MySQLdb



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

    event_list.sort(key=lambda e: get_event_start_datetime(e['folder']))

    return jsonify(event_list), 200

@app.route('/api/rezultate', methods=['POST'])
def rezultate():
    link = request.form.get('link')
    id = request.form.get('id')

    return jsonify({'link': link, 'id': id}), 200

@app.route('/create', methods=['GET', 'POST'])
def index():
    if 'logged_in' not in session or not session['logged_in']:  # Check session variable
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

        # Insert event name into subiecte table
        teste_files = request.files.getlist('teste')
        file_data_list = []

        for file in teste_files:
            if file:
                file_path = os.path.join(directory, file.filename)
                file.save(file_path)
                with open(file_path, "r") as f:
                    file_data = json.load(f)
                    file_data_list.append(file_data)

        # Insert event name into subiecte table
        query = "INSERT INTO subiecte (nume, teste) VALUES (%s, %s)"
        values = (name, json.dumps(file_data_list))
        cursor.execute(query, values)
        db.commit()

        # Delete teste files locally
        for file in teste_files:
            if file:
                os.remove(os.path.join(directory, file.filename))
    return render_template('index.html')

@app.route('/events', methods=['GET'])
def events():
    event_folders = [folder for folder in os.listdir('.') if folder.startswith('event')]
    event_folders.sort(key=lambda folder: get_event_start_datetime(folder))
    return render_template('events.html', event_folders=event_folders)

def get_event_start_datetime(folder):
    folder_datetime = folder[-8:]
    start_datetime = datetime.strptime(folder_datetime, '%d%m%H%M')
    return start_datetime

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

    time_difference = (current_datetime - folder_datetime).total_seconds() / 3600
    print(time_difference*60)

    if time_difference*60 < 0:
        # return send_from_directory(event_folder, file)
        return (f"Acest eveniment incepe in {int(time_difference)} ore si {int((time_difference* 60)%60)} minute", 423)
    elif time_difference*60 > 100000:
        return 'Acest eveniment s-a terminat', 423
    elif time_difference*60 < 100 and time_difference >= 0:
        return send_from_directory(event_folder, file)


@app.route('/', methods=['GET'])
def home():
    if 'logged_in' in session and session['logged_in']:
        return redirect(url_for('events'))
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
            
            # Auto log in after registration
            session['logged_in'] = True
            return redirect(url_for('events'))
        except db.connector.Error as err:
            flash('Error: {}'.format(err), 'error')
            return redirect(url_for('register'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)  # Clear session variable
    flash('You have been logged out', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host = '192.168.1.7', port=80, debug=True)
