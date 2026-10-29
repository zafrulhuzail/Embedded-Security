#!/usr/bin/python3

import socket
import hashlib

ip = '192.168.13.17'

with open('identity', 'rb') as idfile:
    id = idfile.read()

with open('authkey', 'rb') as authkey:
    key = authkey.read()

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect((ip, 5555))
print('Client started ...')

print('Sending authentication request to authentication server in order to receive current system time ...')
clientsocket.send(id)

challenge = clientsocket.recv(64)
print('Received challenge: ' + challenge.decode())

response = hashlib.sha256(challenge + key).hexdigest()
print('Created response: ' + response)

print('Sending response back to authentication server ...')
clientsocket.send(response.encode())

print('Waiting for authentication ...')
authmsg = clientsocket.recv(50)
if authmsg.decode() == 'AUTHENTICATION ERROR!':
    print('AUTHENTICATION ERROR!')
else:
    print('AUTHENTICATION SUCCESS!')
    print('Received authentication server system time: ' + authmsg.decode())

clientsocket.close()
