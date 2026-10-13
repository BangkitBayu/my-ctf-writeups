# Shift Registers

### Category 
Cryptography

### Description
> I learned about lfsr today in school so i decided to implement it in my program. It must be safe right?

### Author
Philip Thayer

### Source
[shift-registers](https://learn.cylabacademy.org/library/716?page=1&category=2&workspace=true&difficulty=2.

Diberikan chall.py sebagai berikut:
```python
from Crypto.Util.number import bytes_to_long, long_to_bytes
from Crypto.Random import get_random_bytes

key = bytes_to_long(get_random_bytes(126))

def steplfsr(lfsr):
b7 = (lfsr >> 7) & 1
b5 = (lfsr >> 5) & 1
b4 = (lfsr >> 4) & 1
b3 = (lfsr >> 3) & 1

feedback = b7 ^ b5 ^ b4 ^ b3
lfsr = (feedback << 7) | (lfsr >> 1)
return lfsr

def encrypt_lfsr(pt_bytes):
output = bytearray()
lfsr = key & 0xFF
for p in pt_bytes:
	lfsr = steplfsr(lfsr)
	ks = lfsr
	output.append(p ^ ks)
	return bytes_to_long(bytes(output))
	
	pt = b"[redacted]"
	ct = encrypt_lfsr(pt)
	
	print(long_to_bytes(ct).hex())
	
```
## Exploitation
Saya selesaikan dengan solver berikut:
```python
ct = bytes.fromhex('30cbb50e507774fdafd01e0bfdbc38d5eadf92991cdd347064e37444e517d661cea9')

def steplfsr(lfsr):
b7 = (lfsr >> 7) & 1
b5 = (lfsr >> 5) & 1
b4 = (lfsr >> 4) & 1
b3 = (lfsr >> 3) & 1

feedback = b7 ^ b5 ^ b4 ^ b3
lfsr = (feedback << 7) | (lfsr >> 1)
return lfsr

def decrypt_with_seed(seed):
lfsr = seed
out = bytearray()
for c in ct:
	lfsr = steplfsr(lfsr)
	out.append(c ^ lfsr)
	return bytes(out)
	
	for seed in range(256):
		pt = decrypt_with_seed(seed)
		if pt.startswith(b'academy{'):
			print(pt.decode())
			break
			
```

## Learning Resources
[https://en.wikipedia.org/wiki/Linear-feedback_shift_register](https://en.wikipedia.org/wiki/Linear-feedback_shift_register)
