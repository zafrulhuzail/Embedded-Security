#!/usr/bin/python3

import socket
import secrets
import hashlib
from datetime import datetime, timezone

ip = '192.168.13.17'

with open('identity', 'rb') as idfile:
    id = idfile.read()

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind((ip, 5555))
serversocket.listen(5)
print('Server started ...')

while True:
    clienthandle, addr = serversocket.accept()
    print('Connection from %s' % str(addr))
    
    recv_uid = clienthandle.recv(24)
    print('Received UID: ' + recv_uid.decode())
    
    if recv_uid == id:
        print('Received UID matches known device ID!')

        challenge = secrets.token_hex(32)
        print('Created challenge: ' + challenge)
      
        print('Sending challenge to device ...')
        clienthandle.send(challenge.encode())
      
        with open('authkey', 'rb') as authkey:
            key = authkey.read()
        
        response = clienthandle.recv(64).decode()
        print('Received response: ' + response)
        
        response_expected = hashlib.sha256(challenge.encode() + key).hexdigest()
        print('Expected response: ' + response_expected)
        
        if response == response_expected:
            print('AUTHENTICATION SUCCESS!')
            now = datetime.now(timezone.utc).astimezone()
            timestamp = now.strftime('%Y/%m/%d %H:%M:%S')
            print('Current time: ' + timestamp)
            clienthandle.send(timestamp.encode())
            clienthandle.close()
            break

        else:
            print('AUTHENTICATION ERROR: response does not match expected value!')
            clienthandle.send(b'AUTHENTICATION ERROR!')
            clienthandle.close()

    else:
        print('AUTHENTICATION ERROR: received UID does not match known device ID!')
        clienthandle.send(b'AUTHENTICATION ERROR!')
        clienthandle.close()
