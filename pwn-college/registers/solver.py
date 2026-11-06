val = 0x5e09
val += 0x1f04
val <<= 1
val ^= 0xa7d2
val -= 0x2c3d

# Atur batas ke 32 bit karena DWORD PTR [rbp-0x4]
val &= 0xffffffff
print(hex(val))
