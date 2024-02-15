import socket
import threading
from dnslib import DNSRecord, DNSHeader, DNSQuestion, RR, QTYPE, A, AAAA, NS, CNAME, MX

def handle_dns_request(data, client_address, server_socket):
    dns_request = DNSRecord.parse(data)
    query_name = dns_request.q.qname
    dns_response = dns_request.reply()
    
    with open('bd_auth_records.txt', 'r') as file:
        li = 0
        for line in file:
            if li == 0:
                li += 1
                continue
            parts = line.strip().split()
            if parts[0] == query_name:
                if parts[2] == "A":
                    dns_response.add_answer(RR(parts[0], QTYPE.A, rdata=A(parts[1]), ttl=int(parts[3])))
                    li += 1
                elif parts[2] == "AAAA":
                    dns_response.add_answer(RR(parts[0], QTYPE.AAAA, rdata=AAAA(parts[1]), ttl=int(parts[3])))
                    li += 1
                elif parts[2] == "NS":
                    dns_response.add_answer(RR(parts[0], QTYPE.NS, rdata=NS(parts[1]), ttl=int(parts[3])))
                    li += 1
                elif parts[2] == "CNAME":
                    dns_response.add_answer(RR(parts[0], QTYPE.CNAME, rdata=CNAME(parts[1]), ttl=int(parts[3])))
                    li += 1
                elif parts[2] == "MX":
                    dns_response.add_answer(RR(parts[0], QTYPE.MX, rdata=MX(parts[1]), ttl=int(parts[3])))
                    li += 1
        if li <= 1:
            print('\nNo match in the server. Sending no match found response')
            server_socket.sendto('No match found'.encode('utf-8'), client_address)
        else:
            response_data = dns_response.pack()
            print('\nSending response to {}:{}'.format(*client_address))
            print('Response: ', dns_response, '\n')
            server_socket.sendto(response_data, client_address)

def handle_client_request(server_socket):
    while True:
        data, client_address = server_socket.recvfrom(4096)
        print("\nReceived request from {}: {}".format(*client_address))

        handle_dns_request(data, client_address, server_socket)
    
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 8016)
server_socket.bind(server_address)

print('DNS server running on {}:{}'.format(*server_address))

client_thread = threading.Thread(target=handle_client_request, args=(server_socket,))
client_thread.daemon = False
client_thread.start()
