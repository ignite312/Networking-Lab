import socket

#Connection
HOST_IP = '192.168.0.100'
HOST_PORT = 12348
ENCODER = "utf-8"
BYTESIZE = 1024

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST_IP, HOST_PORT))
server_socket.listen()

print("Server is running... \n")
client_socket, client_address = server_socket.accept()

client_socket.send("You are connected to the server...".encode(ENCODER))

def isPrime(n):
    if n < 2:
        return "No"
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
    print("Received number: ", number)
    op = client_socket.recv(BYTESIZE).decode(ENCODER)
    print("Received request: ", op)

    if op == "quit":
        client_socket.send("quit".encode(ENCODER))
        print("\nEnding the Server... goodbye!")
        break
    elif op == 'Prime':
        message = isPrime(int(number))
        client_socket.send(message.encode(ENCODER))
        print("sent response: ", message)
    elif op == "Palindrome":
        message = isPalindrome(number)
        client_socket.send(message.encode(ENCODER))
        print("sent response: ", message)

server_socket.close()