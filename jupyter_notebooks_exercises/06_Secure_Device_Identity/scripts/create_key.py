#!/usr/bin/env python3

import secrets

auth_key      = secrets.token_hex(32)
auth_key_file = 'authkey'

with open(auth_key_file, 'w') as f:
  f.write(auth_key)

print('Created 32-byte secret key: ' + auth_key)
print('Stored key in file:         ' + auth_key_file)
