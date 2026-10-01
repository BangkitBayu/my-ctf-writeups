import base64

# NILAI AWAL HEX
encoded_text = "72bca9b68fc16ac7beeb8f849dca1d8a783e8acf9679bf9269f7bf"

# UBAH HEX KE BYTES
plain_hex = bytes.fromhex(encoded_text)

encode_b64 = base64.b64encode(plain_hex)

print(f"flag: {encode_b64}")
