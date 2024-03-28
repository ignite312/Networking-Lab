import socket

#Connection
DEST_IP = "192.168.0.100"
DEST_PORT = 12348
ENCODER = "utf-8"
BYTESIZE = 1024

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((DEST_IP, DEST_PORT))

while True:
    message = client_socket.recv(BYTESIZE).decode(ENCODER)

    if message == "quit":
        client_socket.send("quit".encode(ENCODER))
        print("\nEnding the server... goodbye!")
        break
    else:
        print(f"Server: {message}")
        user_input = input(f"\nClient: ")
        client_socket.send(user_input.encode(ENCODER))

client_socket.close()