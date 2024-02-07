import requests
import os

def download_file(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"File downloaded successfully and saved as {save_path}")
    else:
        print(f"Failed to download file: {response.status_code}")

def upload_file(url, file_path):
    with open(file_path, 'rb') as f:
        files = {'file': f}
        headers = {'File-Name': os.path.basename(file_path)}
        response = requests.post(url, files=files, headers=headers)
        print(response.text)

#Connection
HOST_IP = '192.168.0.101'
HOST_PORT = 12348
HOST_URL = f'http://{HOST_IP}:{HOST_PORT}/'

# Download
file_name = input("Enter the file name to download: ")
server_file_url = HOST_URL + "Files/" + file_name
save_path = "Downloads/" + file_name
download_file(server_file_url, save_path)

# Upload
file_name = input("Enter the file name to Upload: ")
client_file_url = "Uploads/" + file_name
upload_path = HOST_URL
upload_file(upload_path, client_file_url)