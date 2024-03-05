import requests

url = 'http://127.0.0.1:5000/upload'

file_path = 'temp.txt'

try:

    with open(file_path, 'rb') as file:

        files = {'file': (file_path, file, 'text/plain')}

        response = requests.post(url, files=files)

        if response.status_code == 200:
            print("File uploaded successfully.")
        else:
            print(f"Failed to upload file. Status code: {response.status_code}")
except FileNotFoundError:
    print(f"The file {file_path} does not exist.")
