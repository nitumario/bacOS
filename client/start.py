import os
import sys
import requests
url = 'http://192.168.241.64/loginapi'

if __name__ == "__main__":
    email = sys.argv[1]
    password = sys.argv[2]



    data = {
        'email': email,
        'password': password
    }

    response = requests.post(url, data=data)

    if response.status_code == 200:
        os.system("mkdir -p /home/participant/" + email)
        os.system("./code")
    elif response.status_code == 401:
        print("Unauthorized")
        os.system("./login")
    else:
        print(f"Unexpected status code: {response.status_code}")

