import socket
import time
from dnslib import DNSRecord, DNSQuestion, QTYPE

def send_dns_query(query_name, client_socket):
    dns_request = DNSRecord.question(query_name)
    dns_request_data = dns_request.pack()
    server_address = ('localhost', 8000)

    start_time = time.time()

    client_socket.sendto(dns_request_data, server_address)
    response_data, _ = client_socket.recvfrom(4096)

    end_time = time.time()

    dns_response = DNSRecord.parse(response_data)

    print('\nReceived DNS response from {}:{}'.format(*server_address))
    print('\nDNS response:\n', dns_response)
    print('\nTime elapsed for the response to be received: ', end_time - start_time)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
query_name = input('Insert a query:\n')
send_dns_query(query_name, client_socket)
