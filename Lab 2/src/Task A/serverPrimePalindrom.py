import socket

#Connection
HOST_IP = "192.168.0.100"
HOST_PORT = 12348
ENCODER = "utf-8"
BYTESIZE = 1024

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST_IP, HOST_PORT))
server_socket.listen()

print("Server is running... \n")
client_socket, client_address = server_socket.accept()

client_socket.send("You are connected to the server...".encode(ENCODER))

while True:
    message = client_socket.recv(BYTESIZE).decode(ENCODER)

    if message == "quit":
        client_socket.send("quit".encode(ENCODER))
        print("\nEnding the Server... goodbye!")
        break
    else:
        print(f"Client: {message}")
        client_socket.send((message.lower()).encode(ENCODER))
        print(f"Sent: {message.lower()}")

server_socket.close()