import socket

HOST_IP = socket.gethostbyname(socket.gethostname())
HOST_PORT = 12345
ENCODER = "utf-8"
BYTESIZE = 1024

# Create a server socket, bind it to an IP/port, and listen
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST_IP, HOST_PORT))
server_socket.listen()

# Accept any incoming connection and let them know they are connected
print("Server is running... \n")
client_socket, client_address = server_socket.accept()

# Send a welcome message to the connected client
client_socket.send("You are connected to the server...".encode(ENCODER))

while True:
    # Receive information from the client
    message = client_socket.recv(BYTESIZE).decode(ENCODER)

    # Quit if the client socket wants to quit, else display the message
    if message.lower() == "quit":
        client_socket.send("quit".encode(ENCODER))
        print("\nEnding the chat... goodbye!")
        break
    else:
        print(f"\n{message}")
        user_input = input("Message: ")
        client_socket.send(user_input.encode(ENCODER))

client_socket.close()
