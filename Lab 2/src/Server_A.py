import socket

HOST_IP = '192.168.5.80'
HOST_PORT = 12348
ENCODER = "utf-8"
BYTESIZE = 1024

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST_IP, HOST_PORT))
server_socket.listen()

print("Server is running... \n")
client_socket, client_address = server_socket.accept()

client_socket.send("You are connected to the server...".upper().encode(ENCODER))


while True:
    message = client_socket.recv(BYTESIZE).decode(ENCODER).upper()

    if message.lower() == "quit":
        client_socket.send("quit".encode(ENCODER))
        print("\nEnding the chat... goodbye!")
        break
    else:
        print(f"\n{message}")
        user_input = input("Server: ")
        client_socket.send(user_input.encode(ENCODER))

server_socket.close()
