import socket
import threading
import json

SERVER_ADDRESS = 'localhost'
SERVER_PORT = 8001

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((SERVER_ADDRESS, SERVER_PORT))

server_socket.listen(5)
print(f'Server listening on {SERVER_ADDRESS}:{SERVER_PORT}...')

def handle_client(client_socket, client_address):
    try:
        request_data = client_socket.recv(1024).decode()
        print(f'Received request from {client_address}:')
        print(request_data)

        if request_data.startswith('OPTIONS'):
            response_headers = 'HTTP/1.1 200 OK\r\n'
            response_headers += 'Access-Control-Allow-Origin: *\r\n'
            response_headers += 'Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS\r\n'
            response_headers += 'Access-Control-Allow-Headers: Content-Type\r\n'
            response_headers += 'Access-Control-Max-Age: 86400\r\n'
            response_headers += '\r\n'

            response = response_headers.encode()
            client_socket.sendall(response)
            return

        requested_resource = request_data.split()[1]

        response_headers = 'HTTP/1.1 200 OK\r\n'
        response_headers += 'Access-Control-Allow-Origin: *\r\n'
        response_headers += 'Content-Type: application/json\r\n\r\n'
        response_body = json.dumps({'resource': requested_resource})

        response = response_headers.encode() + response_body.encode()
        client_socket.sendall(response)

    except Exception as e:
        print(f'Error handling request from {client_address}: {str(e)}')

    finally:
        client_socket.close()

while True:
    print('Waiting for a connection...')
    client_socket, client_address = server_socket.accept()
    print(f'Accepted connection from {client_address}')

    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()