import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = "192.168.0.127"
PORT = 12345
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print(f'Server running on: {HOST}:{PORT}\n')

def send_file(connection, filepath):
    try:
        with open(filepath, 'rb') as file:
            # buffersize = connection.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
            buffersize = 66560
            print(f'buffersize specified by connection: {buffersize}\n')
            data = file.read(buffersize)
            while data:
                connection.send(data)
                # buffersize = connection.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
                print(f'buffersize specified by connection: {buffersize}\n')
                data = file.read(buffersize)
    except Exception as e:
        print('Error sending file: ', e)

connection, client_address = server_socket.accept()
print(f'Accepted connection from {client_address}\nSending Acknowlegment...\n')
connection.send(f'Accepted connection by {HOST}:{PORT}'.encode())
filepath = connection.recv(2048).decode()
send_file(connection, filepath)
server_socket.close()
