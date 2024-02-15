import socket
from dnslib import DNSRecord, DNSQuestion, QTYPE

def is_utf_resp(data):
    try:
        data.decode('utf-8')
        return True
    except Exception:
        return False

def send_dns_query(query_name, client_socket):
    dns_request = DNSRecord.question(query_name)
    dns_request_data = dns_request.pack()
    server_address = ('localhost', 8000)
    while True:
        print('\nSending req to: {}:{}'.format(*server_address))
        client_socket.sendto(dns_request_data, server_address)
        response_data, _ = client_socket.recvfrom(4096)
        
        if is_utf_resp(response_data):
            print('\nReceived DNS response from {}:{}'.format(*server_address))
            if response_data.decode('utf-8') == 'No match found':
                print('Not found\n')
                break
            cont, host, port = response_data.decode('utf-8').strip().split()
            server_address = (host, int(port))
            print('Server found no match\n')
        else:
            dns_response = DNSRecord.parse(response_data)
            print('\nReceived DNS response from {}:{}'.format(*server_address))
            print('\nDNS response:\n', dns_response)
            break

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
query_name = input('Insert a query:\n')
send_dns_query(query_name, client_socket)
