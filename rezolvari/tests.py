
# C:\MinGW\bin\gcc.exe
import subprocess
import MySQLdb
import sys
import os
import urllib.request
import json
import argparse


db = MySQLdb.connect(host="localhost", user="mario", passwd="toor", db="bacos")
cursor = db.cursor()



def compile_cpp(source_file):
    compile_command = f"C:\\MinGW\\bin\\g++.exe {source_file} -o {source_file[:-4]}.exe"
    subprocess.run(compile_command)


def get_tests(subiect_name):
    query = "SELECT teste FROM events WHERE id = %s"
    cursor.execute(query, (subiect_name,))
    result = cursor.fetchone()
    print(result)
    teste_data = json.loads(result[0])
    return teste_data



def run_tests(teste_data, folder_name):
    punctaj = 0
    for file in os.listdir(folder_name):
        if file.endswith('.cpp'):
            compile_cpp(os.path.join(folder_name, file))
    for file in os.listdir(folder_name):
        if file.endswith('.exe'):
            for test in teste_data:
                test_name = test['id']
                test_input = test['input']
                punctaj_test = test['punctaj']
                test_expected_output= test['expected_output']
                if test_name == file:
                    print(f"Running test {test_name} with input {test_input} for file {file}")
                    result = subprocess.run([os.path.join(folder_name, file)], input=test_input, text=True,capture_output=True)
                    actual_output = result.stdout.strip()
                    print(f"Expected output: {test_expected_output}")
                    print(f"Actual output: {actual_output}")
                    if actual_output == test_expected_output:
                        print(f"Test {test_name} passed")
                        punctaj += int(punctaj_test)
                    else:
                        print(f"Test {test_name} failed")
    print(f"Punctaj final: {punctaj}")
    return punctaj

def get_part_after_last_backslash(input_string):
    # Split the string by backslash and return the last part
    parts = input_string.split('\\')
    return parts[-1] if parts else input_string


def main(subiect, username):
    teste_data = get_tests(subiect)
    punctaj = run_tests(teste_data, username)
    query = f"INSERT INTO punctaj (username, event_id, punctaj) VALUES (%s, %s, %s)"

    cursor.execute(query, (get_part_after_last_backslash(username), subiect, punctaj))
    db.commit()
    print(f"Rezultatul a fost inregistrat cu succes pentru subiectul {subiect} si utilizatorul {username}")

if __name__ == "__main__":
    subiect = sys.argv[1]
    username = sys.argv[2]

    main(subiect, username)

#main('73','mario@mail.com')

#get_tests('73')

#run_tests(get_tests('acummergi'), 'mario') 
#print(get_tests('acummergi'))   



#source_file = r'C:\Users\m3m0r\Projects\bacOS\mario\subiect1.cpp'
#compile_cpp(source_file)

#compile_cpp(r'C:\Users\m3m0r\Projects\bacOS\mario\subiect1.cpp')
#compile_cpp(r'C:\Users\m3m0r\Projects\bacOS\mario\subiect2.cpp')

#print(run_tests(get_tests('olimpiada_miau'), 'mario'))