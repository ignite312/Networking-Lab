import socket

def tcp_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind((host, port))

    server_socket.listen(1)

    print("Server is listening on {}:{}".format(host, port))

    while True:
        connection, client_address = server_socket.accept()
        print("Connection from:", client_address)

        try:
            connection.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 4096)

            while True:
                data = connection.recv(1024)
                if not data:
                    break
                print("Received:", data.decode())

                connection.sendall(b"Acknowledgment: " + data)
        finally:
            connection.close()

if __name__ == "__main__":
    host = "127.0.0.1"
    port = 12345
    tcp_server(host, port)
