import socket
import threading

SERVER_IP = socket.gethostbyname(socket.gethostname())
SERVER_PORT = 12345
ENCODER = 'utf-8'
BYTESIZE = 1024

# Create a client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))

def receive_messages():
    while True:
        try:
            message = client_socket.recv(BYTESIZE).decode(ENCODER)
            print(message)
        except Exception as e:
            print(f"Error receiving message: {e}")
            break

def send_messages():
    while True:
        try:
            user_input = input("Type your message: ")
            client_socket.send(user_input.encode(ENCODER))
        except Exception as e:
            print(f"Error sending message: {e}")
            break

# Get the user's name and send it to the server
user_name = input("Enter your name: ")
client_socket.send(user_name.encode(ENCODER))

# Create two threads for sending and receiving messages
receive_thread = threading.Thread(target=receive_messages)
send_thread = threading.Thread(target=send_messages)

# Start the threads
receive_thread.start()
send_thread.start()
