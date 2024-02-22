import socket
import struct
import threading

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = "192.168.0.127"
PORT = 12345
server_socket.bind((HOST, PORT))
server_socket.listen(1024)

print(f'Server running on: {HOST}:{PORT}\n')

def receive_data(client_socket):
    expected_sequence_number = 0
    receive_window_size = 10485
    client_socket.sendall(struct.pack("!I", receive_window_size))
    totalData = b""
    while True:
        sequence_number, = struct.unpack("!I", client_socket.recv(4))
        data, addr = client_socket.recvfrom(receive_window_size)
        print(f'Data sequence {sequence_number} received: from {client_socket}')
        print(f"Length: ", len(data))
        if len(data) == 0:
            break

        # Check for out-of-order packets
        if sequence_number != expected_sequence_number:
            print(f"Received out-of-order packet with sequence number {sequence_number}, expected {expected_sequence_number}")
            acknowledgment_number = expected_sequence_number
        else:
            acknowledgment_number = sequence_number + 1
            totalData += data
        
        client_socket.sendall(struct.pack("!I", acknowledgment_number))

        expected_sequence_number = acknowledgment_number

        if not data:
            break

    if len(totalData):
        print('Recieved the whole data')
        with open("new.pdf", "wb") as file:
            file.write(totalData)

    client_socket.close()
    server_socket.close()


client_socket, client_address = server_socket.accept()
print(f'Accepted connection from {client_address}\n')

thread = threading.Thread(target=receive_data, args=(client_socket,))
thread.start()

server_socket.close()
