
# C:\MinGW\bin\gcc.exe
import subprocess
import MySQLdb
import sys
import os
import urllib.request
import json


db = MySQLdb.connect(host="localhost", user="mario", passwd="toor", db="bacOS")
cursor = db.cursor()

#link_file = sys.argv[1]
#subiect = sys.argv[2]
#username = sys.argv[3]
def compile_cpp(source_file):
    compile_command = f"C:\\MinGW\\bin\\g++.exe {source_file} -o {source_file[:-4]}.exe"
    subprocess.run(compile_command)

def download(link, name):
    folder_name = name
    os.makedirs(folder_name, exist_ok=True)
    file_name = link.split('/')[-1]
    file_path = os.path.join(folder_name, file_name)
    urllib.request.urlretrieve(link, file_path)

def get_tests(subiect_name):
    query = "SELECT teste FROM subiecte WHERE nume = %s"
    cursor.execute(query, (subiect_name,))
    result = cursor.fetchone()
    teste_data = json.loads(result[0][1:-1])
    return teste_data



def run_tests(teste_data, folder_name):
    punctaj = 0
    for file in os.listdir(folder_name):
        compile_cpp(os.path.join(folder_name, file))
    for file in os.listdir(folder_name):
        if file.endswith('.exe'):
            for test in teste_data:
                test_name = test['id']
                test_input = test['input']
                punctaj_test = test['punctaj']
                test_expected_output= test['output']
                if test_name == file[:-4]:
                    print(f"Running test {test_name} with input {test_input} for file {file}")
                    result = subprocess.run([os.path.join(folder_name, file)], input=test_input, text=True,capture_output=True)
                    actual_output = result.stdout.strip()
                    print(f"Expected output: {test_expected_output}")
                    print(f"Actual output: {actual_output}")
                    if actual_output == test_expected_output:
                        print(f"Test {test_name} passed")
                        punctaj += punctaj_test
                    else:
                        print(f"Test {test_name} failed")
    print(f"Punctaj final: {punctaj}")







#run_tests(get_tests('acummergi'), 'mario') 
#print(get_tests('acummergi'))   



#source_file = r'C:\Users\m3m0r\Projects\bacOS\mario\subiect1.cpp'
#compile_cpp(source_file)

compile_cpp(r'C:\Users\m3m0r\Projects\bacOS\mario\subiect1.cpp')
print(run_tests(get_tests('acummergi'), 'mario'))