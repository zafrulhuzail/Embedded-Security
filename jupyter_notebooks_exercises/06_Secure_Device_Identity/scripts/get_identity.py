#!/usr/bin/env python3

import subprocess

output = subprocess.Popen('cat /proc/cpuinfo | grep Serial', shell=True, stdout=subprocess.PIPE)

unique_id      = output.stdout.read().split()[2]
unique_id_file = 'identity'

with open(unique_id_file, 'wb') as f:
  f.write(unique_id)

print('Collected unique ID:        ' + unique_id.decode())
print('Stored unique ID in file:   ' + unique_id_file)
