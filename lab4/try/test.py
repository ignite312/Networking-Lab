from dnslib import DNSRecord, DNSQuestion, DNSHeader, QTYPE, RR, NS, A, DNSLabel

q = DNSRecord.question("abc.com")
a = q.reply()
a.add_answer(*RR.fromZone("abc.com 60 A 1.2.3.4"))
a.pack()