
# C:\MinGW\bin\gcc.exe
import MySQLdb
import sys
import os
import urllib.request


db = MySQLdb.connect(host="localhost", user="mario", passwd="toor", db="bacOS")
cursor = db.cursor()

#link_file = sys.argv[1]
#username = sys.argv[2]

def download(link, name):
    folder_name = name
    os.makedirs(folder_name, exist_ok=True)
    file_name = link.split('/')[-1]
    file_path = os.path.join(folder_name, file_name)
    urllib.request.urlretrieve(link, file_path)

download('https://bashupload.com/lIhuu/1WbDK.pdf', 'mario')

