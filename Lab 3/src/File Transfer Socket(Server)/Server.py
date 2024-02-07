import socket
import threading
import os

#Server Folder
path = 'Files'
files = sorted(os.listdir(path))

def send_file(client_socket, filename, client_address):
    try:
        file_path = os.path.join(path, filename)
        print(f'Sending "{filename}" to {client_address}\n')
        with open(file_path, 'rb') as file:
            data = file.read(1024)
            while data:
                client_socket.send(data)
                data = file.read(1024)
        print(f'{filename} sent successful to {client_address}')
    except FileNotFoundError:
        print("File not found.")

def handle_client(client_socket, client_address):
    print(f"Connection from {client_address}")

    file_list = ':'.join(files)
    client_socket.send(file_list.encode(ENCODER))

    filename = client_socket.recv(BYTESIZE).decode()
    print(f"Client requested file: {filename}")
    send_file(client_socket, filename, client_address)

    client_socket.close()
    print(f"Connection from {client_address} closed\n")


#Connection
HOST_IP = '192.168.0.101'
HOST_PORT = 12346
ENCODER = 'utf-8'
BYTESIZE = 1024

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST_IP, HOST_PORT))
server_socket.listen(5)
print(f"Server Started.....")

while True:
    client_socket, client_address = server_socket.accept()
    client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_handler.start()