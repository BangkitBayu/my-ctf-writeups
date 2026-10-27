from pwn import xor

key1 = bytes.fromhex("a6c8b6733c9b22de7bc0253266a3867df55acde8635e19c73313")
print(f"Key 1: {key1}")

key2_1 = "37dcb292030faa90d07eec17e3b1c6d8daf94c35d4c9191a5e1e"
key2_3 = "c1545756687e7573db23aa1c3452a098b71a7fbf0fddddde5fc1"
flag_key1_2_3 = "04ee9855208a2cd59091d04767ae47963170d1660df7f56f5faf"  

# Finding key 2 with associative operation
key2 = xor(bytes.fromhex(key2_1), key1)
print(f"Key 2: {key2}")

# Finding key 3 with associative operation
key3 = xor(bytes.fromhex(key2_3), key2)
print(f"Key 3: {key3}")

key1_2_3 = xor(bytes.fromhex(key2_1), key3)

print(f"Key123: {key1_2_3}")

flag = xor(bytes.fromhex(flag_key1_2_3), key1_2_3)

print(f"Flag: {flag}")



