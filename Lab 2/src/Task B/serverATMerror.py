import socket
import random
import time

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

errorPercentage = 0.5
balance = 50000 #or whatever 

while True:
    error = random.random()
    print("Error: ", error, "\n")

    if error <= errorPercentage:
        print('Error has occurred!! Waiting for client...')
    else:
        amount = client_socket.recv(BYTESIZE).decode(ENCODER)
        print('\nClient Request Received:\n')
        print(f'Amount: {amount}')
        op = client_socket.recv(BYTESIZE).decode(ENCODER)
        print(f'Requested operation: {op}\n')
        if op == 'quit':
            client_socket.send('quit'.encode(ENCODER))
            print("\nEnding the server... goodbye!")
            break
        elif op == 'wd':
            if balance < int(amount):
                client_socket.send("You have insufficient funds!!".encode(ENCODER))
                print('Insufficient fund responded\n')
            else:
                balance -= int(amount)
                response = "Amount withdrawn: " + str(amount) + "\nBalance: " + str(balance)
                client_socket.send(response.encode(ENCODER))
                print('Successful withdrawal responded\n')
        elif op == 'dp':
            balance += int(amount)
            response = "Amount diposited: " + str(amount) + "\nBalance: " + str(balance)
            client_socket.send(response.encode(ENCODER))
            print('Successful diposition responded\n')

server_socket.close()