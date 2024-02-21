import socket

def tcp_client(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect((host, port))

    try:
        message = b"Hello, server!"
        print("Sending:", message)
        client_socket.sendall(message)

        data = client_socket.recv(1024)
        print("Received acknowledgment:", data.decode())
    finally:
        client_socket.close()

host = "192.168.0.127"
port = 12345
tcp_client(host, port)
