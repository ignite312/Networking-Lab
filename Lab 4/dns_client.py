import socket

def send_dns_query(query_name, server_address, server_port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        client_socket.sendto(query_name.encode('utf-8'), (server_address, server_port))
        response, _ = client_socket.recvfrom(1024)
        print(response.decode('utf-8'))

if __name__ == "__main__":
    SERVER_ADDRESS = 'localhost'
    SERVER_PORT = 5354
    QUERY_NAME = 'cse.du.ac.bd.'

    send_dns_query(QUERY_NAME, SERVER_ADDRESS, SERVER_PORT)
