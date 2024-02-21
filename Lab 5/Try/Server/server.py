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
    print('Aisi to eino')
    expected_sequence_number = 0
    receive_window_size = 1024
    while True:
        data, addr = client_socket.recvfrom(receive_window_size)
        print(f'Data received: {data} from {addr}')
        print(len(data))

        # Unpack sequence number and data
        sequence_number, data = struct.unpack("!II", data[:4])[:2]

        # Check for out-of-order packets
        if sequence_number != expected_sequence_number:
            print(f"Received out-of-order packet with sequence number {sequence_number}, expected {expected_sequence_number}")
            # Handle out-of-order packets as needed (e.g., ignore, request retransmission)
            continue

        # Process received data
        print(f"Received data: {data}")

        # Send acknowledgment for received data
        acknowledgment_number = sequence_number + len(data)
        client_socket.sendall(struct.pack("!I", acknowledgment_number))  # Send acknowledgment number

        # Update expected sequence number
        expected_sequence_number = acknowledgment_number

        # Check if client closed connection
        if not data:
            break

    client_socket.close()
    server_socket.close()


while True:
    client_socket, client_address = server_socket.accept()
    print(f'Accepted connection from {client_address}\nSending Acknowlegment...\n')

    thread = threading.Thread(target=receive_data, args=(client_socket,))
    thread.start()


server_socket.close()
