import socket

def send_dns_query(query_name, server_address, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True: 
        client_socket.sendto(query_name.encode('utf-8'), (server_address, server_port))
        response, _ = client_socket.recvfrom(1024)
        print(response.decode('utf-8'))
        print('Server: ', server_port)
        client_socket.close()
        break
        

if __name__ == "__main__":
    SERVER_ADDRESS = 'localhost'
    SERVER_PORT = 8000
    QUERY_NAME = input()

    send_dns_query(QUERY_NAME, SERVER_ADDRESS, SERVER_PORT)