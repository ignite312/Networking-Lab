import socket
import time
import os

ADDR = ("127.0.0.1", 6676)
def toHeader(seqNum=0, ackNum=0, ack=0, sf=0, rwnd=0, chcksum = 0):
    return seqNum.to_bytes(
        4, byteorder="little") + ackNum.to_bytes(
            4, byteorder="little") + ack.to_bytes(
                1, byteorder="little") + sf.to_bytes(
                    1, byteorder="little") + rwnd.to_bytes(
                        2, byteorder="little") + chcksum.to_bytes(
                            2, byteorder="little")

def fromHeader(segment):
    return int.from_bytes(
        segment[:4], byteorder="little"), int.from_bytes(
            segment[4:8], byteorder="little"), int.from_bytes(
                segment[8:9], byteorder="little"), int.from_bytes(
                    segment[9:10], byteorder="little"), int.from_bytes(
                        segment[10:12], byteorder="little"), int.from_bytes(
                            segment[12:14], byteorder="little")

def calculate_checksum(bytestream):
    if len(bytestream) % 2 == 1:
        bytestream += b'\x00'

    checksum = 0

    for i in range(0, len(bytestream), 2):
        chunk = (bytestream[i] << 8) + bytestream[i+1]
        checksum += chunk

        if checksum > 0xffff:
            checksum = (checksum & 0xffff) + 1

    return ~checksum & 0xffff

#Initializing Socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(ADDR)
server_socket.listen(1)
print("Server is listening...")
client_socket, addr = server_socket.accept()
client_socket.settimeout(100)
print(f"Connected to server on address {addr}")

#Reading Data
file = open('data.txt', 'rb')
file_size = os.path.getsize("data.txt")

#Declaring necessary variables
mss = 8
rwnd = 50
cwnd = mss
ssthreash = 64
dup_ack = 0
last_ack = 0
recv_buffer = 4
window_len = 2 * recv_buffer
seq_num = 0
ack_num = 0
sf = 0
cnt = 0
expected_ack_num = 0
sent_size = 0
alpha = 0.125
beta = 0.25
ssthresh = 8 

estimated_rtt = 0.5
sample_rtt = 0.5
dev_rtt = 0.5

dup_ack_count = 0 
last_ack_number = -1 
last_sequence_number = -1 
timeout=5
start_time = time.time()
real_start_time = start_time
data = file.read(file_size)

in_fast_recovery = False
packet_sent = 0
packet_received = 0
while seq_num<file_size:
    if in_fast_recovery:
        #If in fast recovery wait for acks for all the packets in the cwnd
        try:
            header = client_socket.recv(14)
            seqNum, ack_num, ack, sf, rwnd, chcksum = fromHeader(header)
            packet_received += 1
        except:
            #Handling timeout
            ssthresh = cwnd // 2
            cwnd = mss
            seq_num = last_ack
            print("timeout")
            start_time = time.time()
            in_fast_recovery = False
        if packet_sent == packet_received:
            #Fast recovery ended
            packet_sent = 0
            packet_received = 0
            in_fast_recovery = False
            dup_ack = 0
            ssthresh = cwnd // 2
            cwnd = ssthresh
            seq_num = last_ack   
    else:
        curr = 0
        print(f"Packets sending. Window value: {cwnd}")
        while(curr<window_len and seq_num<file_size):
            #Sending multiple packets in parallel
            send_size = min(mss, len(data)-seq_num)
            client_socket.sendall(toHeader(seq_num, seq_num, 0, 0, 0, 
                    calculate_checksum(data[seq_num:seq_num+send_size])) + data[seq_num:seq_num+send_size])
            curr += send_size
            sent_size += send_size
            packet_sent = send_size
            packet_received = 0
            seq_num += send_size

        expected_ack_num = seq_num
        try:
            #Getting response
            header = client_socket.recv(14)
            seqNum, ack_num, ack, sf, rwnd, chcksum = fromHeader(header)
            packet_received += 1
        except:
            #Handling Timeout
            ssthresh = cwnd // 2
            cwnd = mss
            seq_num = last_ack
            print("timeout")
            start_time = time.time()
        
        #Calculating RTT, EWMA, DEVRTT etc..
        curr_time = time.time()
        sample_rtt = curr_time - start_time
        estimated_rtt = alpha * sample_rtt + (1 - alpha) * estimated_rtt
        dev_rtt = beta * abs(sample_rtt - estimated_rtt) + (1 - beta) * dev_rtt
        timeout = estimated_rtt + 4 * dev_rtt
        
        #Writting them in a file
        with open('sample.txt', 'a') as file:
            file.writelines(f"{sample_rtt}\n")
        with open('estim.txt', 'a') as file:
            file.writelines(f"{estimated_rtt}\n")
        with open('dev.txt', 'a') as file:
            file.writelines(f"{dev_rtt}\n")
        with open('timeout.txt', 'a') as file:
            file.writelines(f"{timeout}\n")

        window_len = min(cwnd, rwnd)
        if ack_num == last_ack:
            #Got duplicate acknowledgement
            dup_ack += 3
        else:
            dup_ack = 0
        
        if ack_num == expected_ack_num:
            #Normal condition
            start_time = time.time()
            if cwnd >= ssthresh:
                cwnd += mss
            else :
                cwnd = min(2 * cwnd, ssthresh)
        
        if dup_ack == 3:
            #Triple duplicate -> enter fast recovery mode
            #print(f"triple {ssthresh} {cwnd}")
            in_fast_recovery = True    

        last_ack = ack_num
        
        if time.time() - start_time > timeout:
            #Handling timeout
            ssthresh = cwnd // 2
            cwnd = mss
            seq_num = last_ack
            print("Timeout!!!")
            start_time = time.time()
        

client_socket.close()
