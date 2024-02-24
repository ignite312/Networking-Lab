import socket
import os

# Define the Folder Name where the downloaded file will be stored
path = 'Downloads'
try:
    os.makedirs(path)
except FileExistsError:
    pass

def receive_file(server_socket, filename):
    ending_string = 'LifeIsEndHere'.encode()
    file_path = os.path.join(path, filename)
    print("Download Started......")
    with open(file_path, 'wb') as file:
        while True:
            data = server_socket.recv(BYTESIZE)
            if data.endswith(ending_string):
                data = data[:-len(ending_string)]
                break
            file.write(data)
        file.write(data)
        print("File downloaded successful")

# Connection
HOST_IP = "192.168.0.100"
HOST_PORT = 8004
ENCODER = 'utf-8'
BYTESIZE = 1024

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST_IP, HOST_PORT))
print(f"Connection Established with Host: {HOST_IP} port: {HOST_PORT}")

# Receive File List
file_list = client_socket.recv(BYTESIZE).decode(ENCODER).split(":")
for file in file_list:
    if file:
        print(file)
while True:
    filename = input("Enter the name of the file to download (type 'Quit' to exit): ")
    if filename.lower() == "quit":
        break
    client_socket.send(filename.encode())
    receive_file(client_socket, filename)

client_socket.close()