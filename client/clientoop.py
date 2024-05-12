from datetime import datetime
import requests
import os

serverip = "127.0.0.1"
serverport = 5000

def server_crawl():
    response = requests.get(f"http://{serverip}:{serverport}/api")
    events = response.json()
    for event in events:
        folder = event['folder']
        files = event['files']
        
        if datetime_difference(current_datetime(), folder_datetime(folder)) = 0 or datetime_difference(current_datetime(), folder_datetime(folder)) >   :
            print(f"Found event folder {folder} with files: {files}")
            for file in files:
                print(f"Downloading file {file}")
                response = requests.get(f"http://{serverip}:{serverport}/events/{folder}/{file}")
                with open(f"{folder}/{file}", "wb") as f:
                    f.write(response.content)
        else:
            print(f"Skipping event folder {folder}")

    if not events:
        print("No events found on the server")
        
