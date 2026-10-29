#!/usr/bin/python3

import socket
from socket import AF_INET, SOCK_STREAM, SO_REUSEADDR, SOL_SOCKET, SHUT_RDWR, SO_LINGER
import ssl
import time
import struct

count = 0

def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    return recvall(sock, msglen)

def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data
    
listen_addr =  '192.168.13.17'
listen_port = 9000
server_cert = 'server.crt'
server_key = 'server.key'
client_certs = 'client.crt'

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.verify_mode = ssl.CERT_REQUIRED
context.load_cert_chain(certfile=server_cert, keyfile=server_key)
context.load_verify_locations(cafile=client_certs)

bindsocket = socket.socket()
bindsocket.bind((listen_addr, listen_port))
bindsocket.listen(10)

try:
    while True:
        print('\nWaiting for client ...')
        newsocket, fromaddr = bindsocket.accept()
        print('\nClient connected: {}:{}'.format(fromaddr[0], fromaddr[1]))

        conn = context.wrap_socket(newsocket, server_side=True)
        print('\nTLS connection established!')
        print('Peer information:')
        peer_info = conn.getpeercert()
        for x in peer_info:
            print(x, ':', peer_info[x])

        print('\nCiphersuite used: {}'.format(conn.cipher()))

        while True:
            try:
                data = recv_msg(conn)
                print('\nMessage received:')
                print(data.decode())
            except:
                break
        
except Exception as err:
    print('\nCaught exception:', err)
