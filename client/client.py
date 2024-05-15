from datetime import datetime
import requests
import os

serverip = "127.0.0.1"
serverport = 5000

def make_workspace(event):
    url = f"http://{serverip}:{serverport}/events/{event}/{event}.json"
    response = requests.get(url)
    file_content = response.content
    os.mkdir(event)
    response = requests.get(f"http://{serverip}:{serverport}/events/{event}/")
    files = response.json()
    for file in files:
        file_url = f"http://{serverip}:{serverport}/events/{event}/{file}"
        response = requests.get(file_url)
        file_content = response.content
        with open(f"{event}/{file}", "wb") as file:
            file.write(file_content)

def get_first_event():
    response = requests.get(f"http://{serverip}:{serverport}/api")
    event_list = response.json()
    return event_list[0]['folder']


def wait_for_event(event):
    response = requests.get(f"http://{serverip}:{serverport}/api/events/{event}.json")
    while(response.status_code == 423):
        os.run("./waiting.sh")
    if(response.status_code == 200):
        start_event(event)

def start_event(event):
    make_workspace(event)
    
def start_ide(event):
    response = requests.get(f"http://{serverip}:{serverport}/api")
    response = response.json()
    pdf_files = []
    for x in response:
        if(x['folder'] == event):
            for file in x['files']:
                if(file.endswith(".pdf")):
                    pdf_files.append(file)

    pdf_files = " ".join(pdf_files)




#print(datetime_difference(current_datetime(), folder_datetime("event_asd_14050105")))
start_ide('event_asd_14051212')
