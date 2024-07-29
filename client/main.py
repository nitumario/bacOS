import os
import sys
import requests
url = 'http://192.168.0.54/'

if __name__ == "__main__":
    code = sys.argv[1]
    startdatetime = requests.get(url + 'startdatetime/' + code).json()
    
    folder_path = '/home/participanti'
    if os.path.isdir(folder_path):
        folder_list = os.listdir(folder_path)
        if len(folder_list) == 1 and os.path.isdir(os.path.join(folder_path, folder_list[0])):
            workspace = os.path.join(folder_path, folder_list[0])
            subiecte = requests.get(url + 'subiecte/' + code).json()
            for subiect in subiecte:
                subiect_url = url + 'event/' + code + '/' + subiect
                response = requests.get(subiect_url)
                if response.status_code == 200:
                    subiect_content = response.content
                    subiect_path = os.path.join(workspace, subiect)
                    with open(subiect_path, 'wb') as file:
                        file.write(subiect_content)
                    subiect_path_cpp = subiect_path[:-3] + 'cpp'
                    with open(subiect_path_cpp, 'wb') as file_cpp:
                        file_cpp.write(subiect_content)
        
    durata = requests.get(url + 'durata/' + code).json()
    compiler = requests.get(url + 'compiler/' + code).json()


