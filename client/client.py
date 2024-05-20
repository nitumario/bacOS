from datetime import datetime
import requests
import os
import time
import subprocess
import tkinter as tk
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget

class Event:
    def __init__(self, ip, nume):
        self.ip = ip
        self.serverport = 80
        self.nume = nume
        self.username = "miaumiau"
        self.path = f"~/Desktop/{self.nume}/"
        api_json = requests.get(f"http://{self.ip}:{self.serverport}/api")
        api_json = api_json.json()
        self.subiecte = []
        for subiecte in api_json:
            if subiecte['folder'] == self.nume:
                for fisier in subiecte['files']:
                    if fisier.endswith(".pdf"):
                        self.subiecte.append(f"{fisier}")

        self.subiecte_wpath = []

        for subiecte in api_json:
            if subiecte['folder'] == self.nume:
                for fisier in subiecte['files']:
                    if fisier.endswith(".pdf"):
                        self.subiecte_wpath.append(f"{self.path}{fisier[:-4]}/{fisier}")

    def wait(self):
        process = None
        while True:
            response = requests.get(f"http://{self.ip}:{self.serverport}/events/{self.nume}/{self.nume}.json")
            if response.status_code == 423 and process is None:
                process = subprocess.Popen(["python3", "waiting.py"])
            elif response.status_code == 200:
                if process is not None:
                    process.terminate()
                self.start()
                break  
            time.sleep(1)  

    def make_workspace(self):
        url = f"http://{self.ip}:{self.serverport}/events/{self.nume}/{self.nume}.json"
        response = requests.get(url)
        file_content = response.content
        self.path = os.path.expanduser(self.path)
        os.mkdir(self.path)

        for subiect, subiect_wopath in zip(self.subiecte_wpath, self.subiecte):
            subiect_folder = os.path.join(self.path, os.path.basename(subiect)[:-4])
            os.mkdir(subiect_folder)
            cpp_filename = os.path.join(subiect_folder, os.path.basename(subiect_folder) + ".cpp")
            with open(cpp_filename, 'w') as cpp_file:
                cpp_file.write("\n")
            file_url = f"http://{self.ip}:{self.serverport}/events/{self.nume}/{subiect_wopath}"
            subprocess.run(["wget", "-P", subiect_folder, file_url]) 

    def start_ide(self):
        self.durata = None
        self.compiler = None
        response = requests.get(f"http://{self.ip}:{self.serverport}/events/{self.nume}/{self.nume}.json")
        event_data = response.json()
        self.durata = event_data['durata']
        self.compiler = event_data['compiler']

        cpp_file_paths = [os.path.splitext(path)[0] + ".cpp" for path in self.subiecte_wpath]
        file_paths_str = " ".join([os.path.abspath(path) for path in cpp_file_paths])
        #print("codeblocks", *file_paths_str)
        ide = subprocess.Popen(["codeblocks", *cpp_file_paths], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        pdfs = []
        for pdf in self.subiecte_wpath:
            pdfs.append(os.path.expanduser(pdf))
        pdf_viewer = subprocess.Popen(["evince", *pdfs], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        #print("evince", pdfs)
        #pdf_viewer = subprocess.Popen(["evince " + pdfs], shell = True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        #time.sleep(float(self.durata) * 60)  
        time.sleep(5)
        ide.terminate()
        self.end_event()

    def end_event(self):
        time.sleep(5)
        cpp_file_paths = [os.path.splitext(path)[0] + ".cpp" for path in self.subiecte_wpath]
        print(cpp_file_paths)
        for file in cpp_file_paths:
            print(f"Uploading {file}")
            # Use a single string for the command with shell=True
            command = f"bash /home/m3m0r14l/Desktop/bacOS/client/upload.sh {file} {self.username} {self.nume}"
            subprocess.Popen(command, shell=True)
            time.sleep(10)
        # Run the final command
        final_command = f"bash /home/m3m0r14l/Desktop/bacOS/client/upload.sh done {self.username} {self.nume}"
        subprocess.Popen(final_command, shell=True)
        #process.terminate()
        
    def start(self):
        self.make_workspace()
        self.start_ide()

app = QApplication([])
window = QMainWindow()
window.setWindowTitle("Event Start")
window.setGeometry(100, 100, 300, 150)

widget = QWidget()
layout = QVBoxLayout()

label = QLabel()
label.setText("Codul evenimentului:")
layout.addWidget(label)

input_box = QLineEdit()
layout.addWidget(input_box)

button = QPushButton()
button.setText("Porneste evenimentul")
layout.addWidget(button)

def start_event():
    event_name = input_box.text()
    event = Event("192.168.1.7", event_name)
    event.wait()
    window.close()  

button.clicked.connect(start_event)

widget.setLayout(layout)
window.setCentralWidget(widget)

window.show()
app.exec()