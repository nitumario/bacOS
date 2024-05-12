from flask import Flask, request, render_template, send_from_directory, jsonify
from datetime import datetime
import os
import json

app = Flask(__name__)

@app.route('/api', methods=['GET'])
def api():
    event_folders = [folder for folder in os.listdir('.') if folder.startswith('event')]
    event_list = []

    for folder in event_folders:
        event = {}
        event['folder'] = folder
        event['files'] = os.listdir(folder)
        event_list.append(event)

    return jsonify(event_list)


@app.route('/', methods=['GET', 'POST'])
def index():
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

        event_data = {
            "name": name,
            "start_date": formatted_date,
            "start_time": formatted_time,
            "durata": durata,
            "compiler": compiler
        }

        with open(f"{directory}/event{ziua_start}{luna_start}{ora_start}{minut_start}.json", "w") as f:
            json.dump(event_data, f)

        for i in range(1, 4):
            file = request.files.get(f'file{i}')
            if file:
                file.save(os.path.join(directory, file.filename))

    return render_template('index.html')

@app.route('/events', methods=['GET'])
def events():
    event_folders = [folder for folder in os.listdir('.') if folder.startswith('event')]
    return render_template('events.html', event_folders=event_folders)

@app.route('/events/<event_folder>', methods=['GET'])
def see_contents(event_folder):
    full_path = os.path.join('.', event_folder)
    files = os.listdir(full_path)
    
    return render_template('event.html', files=files, event_folder=event_folder)

@app.route('/events/<event_folder>/<file>', methods=['GET'])
def download_file(event_folder, file):
    if file.endswith('.json'):
        return send_from_directory(event_folder, file)
    else:
        folder_datetime = event_folder[-8:]

        current_datetime = datetime.now()
        current_datetime = current_datetime.strftime('%d%m%H%M')

        if folder_datetime == current_datetime:
            return send_from_directory(event_folder, file)
        else:
            return "File can only be downloaded if the folder date and time match the current date and time."

if __name__ == '__main__':
    app.run(debug=True)
