from datetime import datetime
import requests
import os
import time
import subprocess

class Event:
    def __init__(self, ip, nume):
        self.ip = ip
        self.serverport = 80
        self.nume = nume
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
        print("codeblocks", file_paths_str)

        ide = subprocess.Popen(["codeblocks", *cpp_file_paths])
        time.sleep(int(self.durata) * 60)  
        ide.terminate()

    def start(self):
        self.make_workspace()
        self.start_ide()

olimpiada = Event("192.168.1.7", "event_asdas_17050240")
olimpiada.wait()
