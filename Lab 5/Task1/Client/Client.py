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
        client_socket.sendall(struct.pack("!I", sequence_number))
        client_socket.send(packet)

        acknowledgment_number, = struct.unpack("!I", client_socket.recv(4))
        print(f'Received acknowledged sequence number: {acknowledgment_number}')

        if acknowledgment_number == len(data):
            client_socket.sendall(struct.pack("!I", 0))
            packet = b""
            client_socket.sendall(packet)
            break

        sequence_number = acknowledgment_number

window_size, = struct.unpack("!I", client_socket.recv(4))
print(f'Server specified window size: {window_size}\n')

data = []
with open("something.pdf", "rb") as file:
    buff = file.read(window_size)
    while len(buff):
        data.append(buff)
        buff = file.read(window_size)

send_data(data)

client_socket.close()
