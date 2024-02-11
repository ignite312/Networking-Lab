import socket
import time

def load_dns_records(file_path):
    """
    Load DNS records from the provided file, skipping the header line.
    """
    dns_records = {}

    with open(file_path, 'r') as file:
        next(file)  # Skip the header line
        for line in file:
            parts = line.strip().split()
            name = parts[0]
            value = parts[1]
            record_type = parts[2]
            try:
                ttl = int(parts[3])
            except ValueError:
                # If TTL cannot be converted to an integer, set it to a default value
                ttl = 86400  # Default TTL value

            if name not in dns_records:
                dns_records[name] = []

            dns_records[name].append((value, record_type, ttl))

    return dns_records

def handle_dns_query(query_name, dns_records):
    """
    Handle DNS queries based on the loaded DNS records.
    """
    if query_name in dns_records:
        return dns_records[query_name]
    else:
        return []
    

def delete_line(file_path, elapsed_time):
    # Read the file
    with open(file_path, 'r') as file:
        lines = file.readlines()
    line_numbers = []
    i = 0
    for line in lines:
        i += 1
        words = line.split(' ')
        if int(words[-1]) >= elapsed_time:
            line_numbers.append(i)

    # Remove the line
    for line_number in line_numbers:
        if 0 < line_number <= len(lines):
            del lines[line_number - 1]
        else:
            print("Line not deleted")

    with open(file_path, 'w') as file:
        file.writelines(lines)

def start_dns_server(file_path):
    """
    Start the DNS server with the provided DNS records file.
    """
    dns_records = load_dns_records(file_path)
    DNS_PORT = 8000         #root

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind(('localhost', DNS_PORT))
        print(f"DNS server started. Listening on port {DNS_PORT}...")
        start_time = time.time()
        elapsed_time = 0
        while True:
            data, addr = server_socket.recvfrom(1024)
            query_name = data.decode('utf-8').strip()

            current_time = time.time()

            if current_time - start_time >= 1:
                elapsed_time += 1


            response = handle_dns_query(query_name, dns_records)

            if response:
                # Send DNS response
                response_str = '\n'.join('\t'.join(map(str, record)) for record in response)
                server_socket.sendto(response_str.encode('utf-8'), addr)
            else:
                server_socket.sendto(query_name.encode('utf-8'), ('localhost', 8001))
                response, _ = server_socket.recvfrom(1024)
                server_socket.sendto(response, addr)

if __name__ == "__main__":
    DNS_RECORDS_FILE = 'resolver_server.txt'
    start_dns_server(DNS_RECORDS_FILE)