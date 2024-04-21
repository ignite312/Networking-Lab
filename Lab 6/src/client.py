# client socket program
import socket
import time 
import random

# Function to create TCP segment header
def create_segment(seq_num=0, ack_num=0, ack=0, sf=0, rwnd=0, checksum=0):
    return seq_num.to_bytes(4, byteorder="little") + \
           ack_num.to_bytes(4, byteorder="little") + \
           ack.to_bytes(1, byteorder="little") + \
           sf.to_bytes(1, byteorder="little") + \
           rwnd.to_bytes(2, byteorder="little") + \
           checksum.to_bytes(2, byteorder="little")

# Function to extract header fields from TCP segment
def extract_header(segment):
    return int.from_bytes(segment[:4], byteorder="little"), \
           int.from_bytes(segment[4:8], byteorder="little"), \
           int.from_bytes(segment[8:9], byteorder="little"), \
           int.from_bytes(segment[9:10], byteorder="little"), \
           int.from_bytes(segment[10:12], byteorder="little"), \
           int.from_bytes(segment[12:14], byteorder="little")

# Function to calculate checksum
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


HOST = '127.0.0.1'
PORT = 6676

def main():
    # create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connection to hostname on the port.
    client_socket.connect((HOST, PORT))

    recv_buffer_size = 64
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, recv_buffer_size)

    # Initialize parameters
    expected_seq_num = 0
    ack_num = 0
    start_time = time.time()
    client_socket.settimeout(1)

    # Initialize data variables
    received_data = b''
    buffer_data = b''
    mss = 8


    while True:
            try:
                # Receive TCP segment header
                header = client_socket.recv(14)
                seq_num, ack_num, ack, sf, rwnd, checksum = extract_header(header)
                if not header:
                    break
                print("New seq_num: ",seq_num)
                print("expected_seq_num: ",expected_seq_num)
                # Receive data
                data = client_socket.recv(mss)
                print(data)
                
                # Verify checksum
                if calculate_checksum(data) != checksum:
                    continue
            except:
                # Handle timeout
                rwind = recv_buffer_size - (len(buffer_data) + mss - 1) // mss
                # print("Timeout Happened. New rwind: ", rwind)
                try:
                    # Send acknowledgment with updated receive window size
                    to_send_ack = create_segment(expected_seq_num, ack_num, 1, 0, rwind, 0)
                    client_socket.sendall(to_send_ack)
                except:
                    print("Connection closed")
                start_time = time.time()
                continue

            if not data:
                break
            
            # Process received data
            seq_num = ack_num
            val = random.randint(0, 20)
            if val > 1:
                if seq_num == expected_seq_num:
                    buffer_data += data
                    ack_num += len(data)
                    expected_seq_num += len(data)
                    to_send_ack = create_segment(seq_num, ack_num, 1, 0, 8, 0)
                    if len(buffer_data) >= recv_buffer_size:
                        received_data += buffer_data
                        buffer_data = b''
                        try:
                            # Send acknowledgment if buffer is full
                            client_socket.sendall(to_send_ack)
                        except:
                            print("Client closed")
                else:
                    # Triple duplicate acknowledgment
                    print("Triple duplicate acknowledgment Happened. Sending acknowledgment.")
                    to_send_ack = create_segment(expected_seq_num, expected_seq_num, 1, 1, 0, 0)
                    client_socket.sendall(to_send_ack)
            elif val > 0:
                time.sleep(6)
            else:
                print("Triple duplicate acknowledgment Happened. Sending acknowledgment.")
                to_send_ack = create_segment(expected_seq_num, expected_seq_num, 1, 1, 0, 0)
                client_socket.sendall(to_send_ack)      

    # Process remaining data in buffer
    received_data += buffer_data
    print(received_data.decode())

    # Close client and server sockets
    client_socket.close()
    


if __name__ == '__main__':
    main()
    
