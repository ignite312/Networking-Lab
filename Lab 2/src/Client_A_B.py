import socket

#DEST_IP = socket.gethostbyname(socket.gethostname())

DEST_IP = '10.33.2.94'
DEST_PORT = 12348
ENCODER = "utf-8"
BYTESIZE = 1024

# Create a client socket and connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((DEST_IP, DEST_PORT))

while True:
    # Receive information from the server
    message = client_socket.recv(BYTESIZE).decode(ENCODER)

    # Quit if the connected server wants to quit, else keep sending messages
    if message.lower() == "quit":
        client_socket.send("quit".encode(ENCODER))
        print("\nEnding the chat... goodbye!")
        break
    else:
        print(f"\n{message}")
        user_input = input("Amount: ")
        client_socket.send(user_input.encode(ENCODER))
        user_input = input("Operation Type: ")
        client_socket.send(user_input.encode(ENCODER))

client_socket.close()
