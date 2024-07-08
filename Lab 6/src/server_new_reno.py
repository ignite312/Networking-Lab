import socket
import threading
import os
import time
from typing import Tuple
import traceback
from select import select
from enum import Enum

class State(Enum):
   SLOW_START = 0
   FAST_RECOVERY = 1
   CONGESTION_AVOIDANCE = 2

class colors:
   RED = '\033[91m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   BLUE = '\033[94m'
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   END = '\033[0m'

ENCODER = 'utf-8'

cwnd = 1
state = State.SLOW_START
ssthreshold = 32
MSS = 1024
PACKET_SIZE = 1111
HEADER_LENGTH = 87
last_packet_acked = 1
last_packet_sent = 0
buffer = {}
dup_ack_count = {}
fast_recovery_limit = 0

start_time = time.time()
estimated_rtt = 20
dev_rtt = 0
ALPHA = 0.125
BETA = 0.25

timeout = 0.1

def handle_rtt(ack_no: int):
   global estimated_rtt, dev_rtt
   sample_rtt = (time.time() - start_time) * 1000
   estimated_rtt = (1 - ALPHA) * estimated_rtt + ALPHA * sample_rtt
   dev_rtt = (1 - BETA) * dev_rtt + BETA * abs(estimated_rtt - sample_rtt)
   print(f"sample_rtt: {sample_rtt}ms, est_rtt: {estimated_rtt}ms, dev_rtt = {dev_rtt}ms")

def make_packet(data: bytes, sequence_number: int):
   source_port = b'0000008989'
   destination_port = b'0000008989'
   sequence_number = str(sequence_number).zfill(20).encode(ENCODER)
   ack_number = b'00000000000000000000'
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
   header_length = int(packet[60:76].decode(ENCODER))
   ack_flag = int(packet[76:77].decode(ENCODER))
   rwnd = int(packet[77:87].decode(ENCODER))
   data = packet[87:]

   return source_port, destination_port, sequence_number, ack_number, header_length, ack_flag, rwnd, data

def get_file_size(file_path):
   # Get the size of the file in bytes
   size = os.path.getsize(file_path)
   return size

def calculate_total_packets(file_path):
   file_size = get_file_size(file_path)
   total_packets: int = file_size / MSS
   if file_size % MSS != 0:
      total_packets += 1
   return total_packets

def extract_initial_info(data: str):
   parsed_data = data.split(',')
   return (parsed_data[0], parsed_data[1])

def handle_client(client_socket: socket, addr: tuple):
   try:
      data = client_socket.recv(1024)
      decoded_data = data.decode(ENCODER)
      print(f"received data from {addr}: {decoded_data}")
    
      filename, rwnd = extract_initial_info(decoded_data)
      print(f"filename: {filename}, rwnd: {rwnd}")
      send_data(client_socket, filename, rwnd)
   except Exception as e:
      print(f"Error handling client: {e}")
      traceback.print_exc()
   finally:
      client_socket.close()

def send_file_data(client_socket: socket, file):
   data = file.read(MSS)
   sequence_number = last_packet_sent + 1
   buffer[sequence_number] = data
   packet = make_packet(data, sequence_number)

   global start_time
   start_time = time.time()

   client_socket.send(packet)
   print(colors.YELLOW + f"sent packet {sequence_number}")

def handle_slow_start(client_socket: socket, filename: str, rwnd: int, file):
   print("state: handle slow start.")
   global cwnd, state
   if cwnd + 1 > ssthreshold:
      state = State.CONGESTION_AVOIDANCE
   else:
      cwnd += 1

def handle_congestion_avoidance(client_socket: socket, filename: str, rwnd: int, file):
   print("state: handle congestion avoidance.")
   global cwnd, state
   cwnd += (1 / cwnd)

def handle_fast_recovery(client_socket: socket, filename: str, rwnd: int, file, ack_no: int):
   print("state: handle fast recovery.")
   global cwnd, state
   if ack_no > fast_recovery_limit:
      state = State.CONGESTION_AVOIDANCE
      return
   cwnd += 1

def retransmit(client_socket: socket, ack_no: int):
   packet = make_packet(buffer[ack_no], ack_no)
   client_socket.send(packet)

def send_data(client_socket: socket, filename: str, rwnd: int):
   global last_packet_acked, last_packet_sent, state, fast_recovery_dup_ack, cwnd, \
      ssthreshold
   try:
      total_packets = calculate_total_packets(filename)
      with open(filename, 'rb') as file:
         while True:
            global last_packet_sent
            curr_cwnd = cwnd
            while last_packet_sent < total_packets and last_packet_sent - last_packet_acked + 1 < curr_cwnd:
               send_file_data(client_socket, file)
               last_packet_sent += 1

            readable, writable, _ = select([client_socket], [], [], timeout)

            # check for time out
            if not readable:
               print(colors.RED + f"Timeout has occured." + colors.END)

               state = State.SLOW_START
               cwnd = 1
               ssthreshold = cwnd / 2
               retransmit(client_socket, last_packet_acked)
               continue

            packet = client_socket.recv(HEADER_LENGTH)
            src_port, dest_port, seq_no, ack_no, length, ack_flag, rwnd, data = extract(packet)
            print(colors.BLUE + f"ack received: {ack_no}, current cwnd: {cwnd}, ssthreshold: {ssthreshold}" + colors.END)
            last_packet_acked = ack_no

            if ack_no not in dup_ack_count: 
               handle_rtt(ack_no)
               dup_ack_count[ack_no] = 0
            else: dup_ack_count[ack_no] += 1

            if dup_ack_count[ack_no] >= 3 and state != State.FAST_RECOVERY:
               state = State.FAST_RECOVERY
               fast_recovery_limit = last_packet_sent
               ssthreshold = cwnd / 2
               cwnd = ssthreshold + 3
               fast_recovery_dup_ack = ack_no
               retransmit(client_socket, last_packet_acked)
               dup_ack_count[ack_no] = 0
               continue


            if ack_no > total_packets:
               print(colors.GREEN + "Entire file is successfully sent." + colors.END)
               client_socket.send("END".encode(ENCODER))
               break

            if state == State.SLOW_START:
               handle_slow_start(socket, filename, rwnd, file)
            if state == State.FAST_RECOVERY:
               handle_fast_recovery(socket, filename, rwnd, file, ack_no)
            if state == State.CONGESTION_AVOIDANCE:
               handle_congestion_avoidance(socket, filename, rwnd, file)
         

   except FileNotFoundError:
      print(f"File not found: {filename}")
      traceback.print_exc()
   except Exception as e:
      print(f"Error sending file: {e}")
      traceback.print_exc()
   finally:
      client_socket.close()
      file.close()

def main():
   host = '192.168.0.195'
   port = 8000

   server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
   server_socket.bind((host, port))
   server_socket.listen(5)

   print(f"[*] Listening on {host}:{port}")

   try:
      client_socket, addr = server_socket.accept()
      print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")
      handle_client(client_socket, addr)
   except Exception as e:
      print("\n[*] Server shutting down.")
   finally:
      server_socket.close()

if __name__ == "__main__":
   main()