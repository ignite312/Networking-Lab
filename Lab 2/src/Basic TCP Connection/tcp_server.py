import socket

# Create a server socket, bind it to an IP/port, and listen
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((socket.gethostbyname(socket.gethostname()), 12345))
server_socket.listen()

# Accept a connection from a client
client_socket, client_address = server_socket.accept()

# Print client socket information
print(client_socket)
print(f"Connected to {client_address}\n")

# Send a welcome message to the connected client
client_socket.send("You are now connected!".encode("utf-8"))

# Close the server socket
server_socket.close()