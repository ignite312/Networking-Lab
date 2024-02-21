import socket
import struct

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = "192.168.0.127"
PORT = 12345
client_socket.connect((HOST, PORT))

def send_data(data):
    sequence_number = 0

    while True:
        packet = data[sequence_number]
        client_socket.send(str(sequence_number).encode())
        client_socket.sendall(packet)

        acknowledgment_number = struct.unpack("!I", client_socket.recv(4))
        print(f'Received acknowledged sequence number: {acknowledgment_number}')

        if acknowledgment_number == len(data)-1:
            packet = struct.pack("!II", -1, -1) + b""
            client_socket.sendall(packet)
            break

        sequence_number = acknowledgment_number + 1

window_size = int(client_socket.recv(1024).decode())
print(f'Server specified window size: {window_size}\n')

data = []
with open("book.pdf", "rb") as file:
    buff = file.read(window_size)
    while len(buff):
        data.append(buff)
        buff = file.read(window_size)

send_data(data)

client_socket.close()
