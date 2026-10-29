#!/usr/bin/python3

import socket
import ssl
import time
import struct

def send_msg(sock, msg):
    # Prefix each message with a 4-byte length (network byte order)
    msg = struct.pack('>I', len(msg)) + msg #big-endian = network byte order, unsigned int = 4 byte
    sock.sendall(msg)

host_addr = '192.168.13.17'
host_port = 9000
server_sni_hostname = 'VM-Server'
client_cert = 'stm32mp1.crt'
client_key = 'stm32mp1.key'
ca_cert = 'ca.crt'

context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=ca_cert)
#context.check_hostname = False #hostname check must be disabled, otherwise error --> TODO
context.load_cert_chain(certfile=client_cert, keyfile=client_key)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn = context.wrap_socket(s, server_side=False, server_hostname=server_sni_hostname)
conn.connect((host_addr, host_port))
print('\nTLS connection established!')
print('Peer information:')
peer_info = conn.getpeercert()
for x in peer_info:
    print(x, ':', peer_info[x])

print('\nCiphersuite used: {}'.format(conn.cipher()))

message = b'Hello Server! (supported by CA!)'
print('\nSending message:', message.decode())
send_msg(conn, message)

time.sleep(1)

print('\nClosing connection...')
conn.close()
