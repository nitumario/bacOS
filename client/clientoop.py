from datetime import datetime
import requests
import os
import time
import subprocess

class Event:
    def __init__(self, ip, nume):
        self.ip = ip
        self.serverport = 5000
        self.nume = nume
        self.durata = None
        self.compiler = None
        api_json = requests.get(f"http://{self.ip}:{self.serverport}/api")
        api_json = api_json.json()
        self.subiecte = []
        self.path = f"~/Desktop/{self.nume}/"
        for subiecte in api_json:
            if subiecte['folder'] == self.nume:
                self.durata = subiecte['durata']
                self.compiler = subiecte['compiler']
                for fisier in subiecte['files']:
                    if fisier.endswith(".pdf"):
                        self.subiecte.append(f"{self.path}{fisier}")
        self.subiecte = " ".join(self.subiecte)



    def wait(self):
        response = requests.get(f"http://{self.ip}:{self.serverport}/api/events/{self.nume}.json")
        while(response.status_code == 423):
            process = subprocess.Popen(["./waiting.sh", self.subiecte])
        process.terminate()
        if(response.status_code == 200):
            self.start()

    def make_workspace(self):
        url = f"http://{self.ip}:{self.serverport}/events/{self.nume}/{self.nume}.json"
        response = requests.get(url)
        file_content = response.content
        os.mkdir(self.path)  # Modified line
        response = requests.get(f"http://{self.ip}:{self.serverport}/events/{self.nume}/")
        files = response.json()
        for file in files:
            file_url = f"http://{self.ip}:{self.serverport}/events/{self.nume}/{file}"
            response = requests.get(file_url)
            file_content = response.content
            with open(f"{self.path}/{file}", "wb") as file:  
                file.write(file_content)

    def start_ide(self):
        process = subprocess.Popen(["codeblocks", self.subiecte])
        time.sleep(self.durata * 60)  # Convert duration to seconds
        process.terminate()

    def start(self):
        self.make_workspace()
        self.start_ide()

olimpiada = Event("192.168.1.7", "event_asd_14051212")
olimpiada.wait()




