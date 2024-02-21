import socket
import random

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = "192.168.0.127"
PORT = 12345
client_socket.connect((HOST, PORT))
acknowledgement = client_socket.recv(1024)
print('Acknowledgement: ', acknowledgement.decode(), '\n')

filepath = input('Enter the filepath: ')
client_socket.send(filepath.encode()) 

with open(filepath, 'wb') as file:
    while True:
        client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, random.randint(1024, 4096))
        data = client_socket.recv(256)
        if not data:
            break
        file.write(data)

client_socket.close()