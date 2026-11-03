#!/usr/bin/env python3

from pwn import xor

c = bytes.fromhex("73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d")
# Xor single bytes dioperasikan dalam 1 bytes/8 bit dengan 256 kemungkinan kombinasi

print(f"Cipher from hex: {c}")

for key in range(256):
	m = ''.join(chr(b ^ key) for b in c)
	if m.isprintable():
		print(f"Key: {key} m: {m}")

