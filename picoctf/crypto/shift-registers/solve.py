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
