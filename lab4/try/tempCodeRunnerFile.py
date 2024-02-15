from dnslib import DNSRecord, DNSQuestion, DNSHeader, QTYPE, RR, DNSLabel

# Create the DNS header
dns_header = DNSHeader(id=1234, qr=1, aa=1, ra=1)

# Create the DNS question
dns_question = DNSQuestion("cse.du.ac.bd.", QTYPE.NS)

# Create the DNS record
ns_rdata = DNSLabel("ns1.cse.du.ac.bd.")
ns_record = RR("cse.du.ac.bd.", QTYPE.NS, rdata=ns_rdata)

# Create the DNS response
dns_response = DNSRecord(header=dns_header, q=dns_question)
dns_response.add_answer(ns_record)

# Print the DNS response
# print(dns_response)
# Convert DNS response to bytes
response_bytes = dns_response.pack()

# Send the response over the network using a socket
# Assuming `sock` is a connected UDP socket
# sock.sendto(response_bytes, (client_ip, client_port))

