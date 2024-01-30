import socket

#DEST_IP = socket.gethostbyname(socket.gethostname())

DEST_IP = '10.33.2.94'
DEST_PORT = 12349
ENCODER = "utf-8"
BYTESIZE = 1024

# Create a client socket and connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((DEST_IP, DEST_PORT))

while True:

    message = client_socket.recv(BYTESIZE).decode(ENCODER)


    if message.lower() == "quit":
        client_socket.send("quit".encode(ENCODER))
        print("\nEnding the chat... goodbye!")
        break
    elif message == "Err":
        print(message)
        user_input = input("Amount: ")
        client_socket.send(user_input.encode(ENCODER))
        user_input = input("Operation: ")
        client_socket.send(user_input.encode(ENCODER))
    else:
        print(f"\n{message}")
        user_input = input("Amount: ")
        client_socket.send(user_input.encode(ENCODER))
        user_input = input("Operation: ")
        client_socket.send(user_input.encode(ENCODER))

client_socket.close()
