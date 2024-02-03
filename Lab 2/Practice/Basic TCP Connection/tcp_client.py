import socket

# Create a client socket and connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((socket.gethostbyname(socket.gethostname()), 12345))

# Receive a message from the server
message = client_socket.recv(1024)

# Print the received message
print(message.decode("utf-8"))

# Close the client socket
client_socket.close()
