import socket
import sys
import time 
import threading
import traceback
import random
 
 
class colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    END = '\033[0m'

SERVER_IP = '192.168.0.195'
SERVER_PORT = 8000
BUFFER_SIZE = '2048'
ERROR_PERCENTAGE = 70

ENCODER = 'utf-8'
FILENAME = "data2.txt"
# FILENAME = "image.jpeg"
MSS = 1024
PACKET_SIZE = 1111
HEADER_LENGTH = 87 # 1111 (packet size) - 1024 (mss)
END_MESSAGE = "END".encode(ENCODER)

last_packet_acked = 1

buffer = {}

def make_packet(data: bytes, ack: int):
   source_port = b'0000008989'
   destination_port = b'0000008989'
   sequence_number = b'00000000000000000000'
   ack_number = str(ack).zfill(20).encode(ENCODER)
   header_length = str(len(data)).zfill(16).encode(ENCODER)
   ack_flag = b'0'
   rwnd = b'0000000000'

   header = source_port + destination_port + sequence_number + ack_number + header_length + ack_flag + rwnd

   packet = header + data

   return packet

def extract(packet):
   source_port = int(packet[:10].decode(ENCODER))
   destination_port = int(packet[10:20].decode(ENCODER))
   sequence_number = int(packet[20:40].decode(ENCODER))
   ack_number = int(packet[40:60].decode(ENCODER))
   length = int(packet[60:76].decode(ENCODER))
   ack_flag = int(packet[76:77].decode(ENCODER))
   rwnd = int(packet[77:87].decode(ENCODER))

   return source_port, destination_port, sequence_number, ack_number, length, ack_flag, rwnd

# writes to file and returns the sequence number of the packet that is expected 
def write_to_file(file):
    seq_no = last_packet_acked
    while seq_no in buffer:
        file.write(buffer[seq_no])
        seq_no += 1
    return seq_no

def error():
    return random.randint(1, 100) <= ERROR_PERCENTAGE

def handle_receive(client_socket):
    global last_packet_acked
    with open('received_' + FILENAME, 'ab') as file:
        file.truncate(0)
        while True:
            packet = client_socket.recv(HEADER_LENGTH)
            if packet == END_MESSAGE:
                print(colors.GREEN + "Entire file received." + colors.END)
                break
            
            while len(packet) != HEADER_LENGTH:
                packet += client_socket.recv(HEADER_LENGTH - len(packet))
                print(colors.BLUE + f"received packet header: {packet}" + colors.BLUE)

            src_port, dest_port, sequence_number, ack_number, length, ack_flag, rwnd = extract(packet)
            data = client_socket.recv(length)
            while len(data) != length: 
                data += client_socket.recv(length - len(data))

            print(colors.BLUE + f"received packet: {sequence_number}" + colors.END)

            if error():
                print(colors.RED + f"Error, sequence number: {sequence_number}" + colors.END)
                continue

            buffer[sequence_number] = data

            if sequence_number < last_packet_acked: 
                continue

            last_packet_acked = write_to_file(file)
            ack_packet = make_packet(b'', last_packet_acked)
            client_socket.send(ack_packet)
            print(colors.YELLOW + f"sent ack: {last_packet_acked}")

    

def main():
    startTime = time.time()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, SERVER_PORT)) 

    global FILENAME
    if len(sys.argv) <= 1:
        print("Error")
        return
    
    FILENAME = sys.argv[1]
 
    message = FILENAME + "," + BUFFER_SIZE
    client_socket.send(message.encode(ENCODER))

    handle_receive(client_socket)
 
    endTime = time.time()
    print(colors.GREEN + f"DOWNLOAD FINISHED. Total time is {(endTime - startTime) * 1000}ms" + colors.END)
 
 
if __name__ == "__main__":
    main()