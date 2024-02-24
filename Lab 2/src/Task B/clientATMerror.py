import socket
import time

#Connection
DEST_IP = '192.168.0.100'
DEST_PORT = 12348
ENCODER = "utf-8"
BYTESIZE = 1024

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((DEST_IP, DEST_PORT))

amount = "0"
opcode = "dp"

start_time = time.time()
end_time = time.time()

requested = False

while True:
    message = client_socket.recv(BYTESIZE).decode(ENCODER)
    if message.lower() == "quit":
        client_socket.send("quit".encode(ENCODER))
        print("\nEnding the server... goodbye!")
        break
    else:
        print(f"\nServer Response:\n{message}")

        if requested:
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"Elapsed: {elapsed_time}")
        
        amount = input("\nAmount: ")
        client_socket.send(amount.encode(ENCODER))
        opcode = input("Type in wd or dp for withdrawal or deposit: ")
        client_socket.send(opcode.encode(ENCODER))
        requested = True
        start_time = time.time()

client_socket.close()