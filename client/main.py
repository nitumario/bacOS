import os
import sys
import requests
import datetime
import subprocess
import time

url = 'http://192.168.0.54/'

if __name__ == "__main__":
    code = sys.argv[1]
    startdatetime_str = requests.get(url + 'startdatetime/' + code).json()
    event_datetime = datetime.datetime.strptime(startdatetime_str, '%Y-%m-%d %H:%M:%S')
    process = subprocess.Popen(["./waiting"])

    try:
        while True:
            current_datetime = datetime.datetime.now()

            time_until_event = event_datetime - current_datetime
            minutes_until_event = time_until_event.total_seconds() / 60

            print(f"Minutes until event: {minutes_until_event:.2f}")

            if minutes_until_event <= 0:
                print("The event has started. Terminating the process.")
                break

            time.sleep(10)

    finally:
        process.terminate()
        process.wait()  

    folder_path = '/home/participanti'
    if os.path.isdir(folder_path):
        folder_list = os.listdir(folder_path)
        if len(folder_list) == 1 and os.path.isdir(os.path.join(folder_path, folder_list[0])):
            workspace = os.path.join(folder_path, folder_list[0])
            subiecte = requests.get(url + 'subiecte/' + code).json()
            subiecte_wpath = []
            cpp_file_paths = []

            for subiect in subiecte:
                subiect_url = url + 'event/' + code + '/' + subiect
                response = requests.get(subiect_url)
                if response.status_code == 200:
                    subiect_content = response.content
                    subiect_path = os.path.join(workspace, subiect)
                    with open(subiect_path, 'wb') as file:
                        file.write(subiect_content)
                    subiecte_wpath.append(subiect_path)
                    
                    # Create empty .cpp file
                    cpp_path = os.path.splitext(subiect_path)[0] + ".cpp"
                    with open(cpp_path, 'w') as cpp_file:
                        cpp_file.write("")  # Write nothing to create an empty file
                    cpp_file_paths.append(cpp_path)
        
            file_paths_str = " ".join([os.path.abspath(path) for path in cpp_file_paths])

            print("Generated cpp file paths:")
            print(file_paths_str)

    durata = requests.get(url + 'durata/' + code).json()
    compiler = requests.get(url + 'compiler/' + code).json()
    if compiler == 1:
        ide = subprocess.Popen(["codeblocks", *cpp_file_paths], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
