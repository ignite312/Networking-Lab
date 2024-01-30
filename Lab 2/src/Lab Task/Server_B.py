import socket

HOST_IP = '10.33.2.94'
HOST_PORT = 12349
ENCODER = "utf-8"
BYTESIZE = 1024

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST_IP, HOST_PORT))
server_socket.listen()

print("Server is running... \n")
client_socket, client_address = server_socket.accept()

client_socket.send("You are connected to the server...".encode(ENCODER))

def isPrime(n):
    i = 2
    while i*i <= n:
        if n%i == 0:
            return "No"
        i += 1
    return "Yes"

def isPalindrome(n):
    if n == n[::-1]:
        return "Yes"
    return "No"

while True:
    number = client_socket.recv(BYTESIZE).decode(ENCODER)
    print("received number: ", number)
    op = client_socket.recv(BYTESIZE).decode(ENCODER)
    print("received request: ", op)

    if op == "quit":
        client_socket.send("quit".encode(ENCODER))
        print("\nEnding the chat... goodbye!")
        break
    elif op == 'pm':
        message = isPrime(int(number))
        client_socket.send(message.encode(ENCODER))
        print("sent response: ", message)
    elif op == "pal":
        message = isPalindrome(number)
        client_socket.send(message.encode(ENCODER))
        print("sent response: ", message)

server_socket.close()
