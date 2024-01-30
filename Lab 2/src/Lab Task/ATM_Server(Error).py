import socket
import random

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

balance = 50000

while True:
    amount = client_socket.recv(BYTESIZE).decode(ENCODER)
    print('Amount: ', amount)
    op = client_socket.recv(BYTESIZE).decode(ENCODER)
    print('Requested operation: ', op)

    error = random.randint(1, 100)

    if error <= 50:
        print('Error Generated!!\n')
        client_socket.send("Err".encode(ENCODER))
    else:
        if op == "quit":
            client_socket.send("quit".encode(ENCODER))
            print("\nEnding the chat... goodbye!")
            break
        elif op == 'wd':
            if balance < int(amount):
                client_socket.send("You have insufficient funds!!".encode(ENCODER))
                print('Insufficient fund responded')
            else:
                balance -= int(amount)
                response = "Amount withdrawn: " + str(amount) + "\nBalance: " + str(balance)
                client_socket.send(response.encode(ENCODER))
                print('Successful withdrawal responded')
        elif op == 'dp':
            balance += int(amount)
            response = "Amount diposited: " + str(amount) + "\nBalance: " + str(balance)
            client_socket.send(response.encode(ENCODER))
            print('Successful diposition responded')
server_socket.close()
