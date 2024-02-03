import socket
import threading

HOST_IP = socket.gethostbyname(socket.gethostname())
HOST_PORT = 12345
ENCODER = 'utf-8'
BYTESIZE = 1024

# Create a server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST_IP, HOST_PORT))
server_socket.listen(5)  # Maximum number of queued connections

# Create two blank lists to store connected client sockets and their names
client_socket_list = []
client_name_list = []

def broadcast_message(message):
    # Send a message to ALL clients connected to the server
    for client_socket in client_socket_list:
        try:
            client_socket.send(message.encode(ENCODER))
        except Exception as e:
            print(f"Error broadcasting message to client: {e}")

def receive_message(client_socket):
    # Receive an incoming message from a specific client and forward the message to be broadcast
    try:
        message = client_socket.recv(BYTESIZE).decode(ENCODER)
        if message:
            print(f"Received message: {message}")
            broadcast_message(f"{client_name_list[client_socket_list.index(client_socket)]}: {message}")
    except Exception as e:
        print(f"Error receiving message from client: {e}")

def connect_client(client_socket):
    # Connect an incoming client to the server
    try:
        client_name = client_socket.recv(BYTESIZE).decode(ENCODER)
        client_name_list.append(client_name)
        client_socket_list.append(client_socket)
        print(f"Client '{client_name}' connected.")
        broadcast_message(f"{client_name} has joined the chat.")
    except Exception as e:
        print(f"Error connecting client: {e}")

def handle_client(client_socket):
    connect_client(client_socket)
    
    while True:
        receive_message(client_socket)

# Main server loop to accept incoming connections
while True:
    client_socket, client_address = server_socket.accept()
    client_handler = threading.Thread(target=handle_client, args=(client_socket,))
    client_handler.start()
