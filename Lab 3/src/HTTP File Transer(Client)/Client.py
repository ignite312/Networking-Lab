import requests

def download_file(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"File downloaded successfully and saved as {save_path}")
    else:
        print(f"Failed to download file: {response.status_code}")
        
#Connection
HOST_IP = '192.168.0.101'
HOST_PORT = 12346
HOST_URL = f'http://{HOST_IP}:{HOST_PORT}/'

file_url = HOST_URL+"Files/A_S.txt"
save_path = "Downloads/A_S.txt"
download_file(file_url, save_path)
