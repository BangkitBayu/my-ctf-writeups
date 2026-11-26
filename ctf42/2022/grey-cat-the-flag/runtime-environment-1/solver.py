c = "GvVf+fHWz1tlOkHXUk3kz3bqh4UcFFwgDJmUDWxdDTTGzklgIJ+fXfHUh739+BUEbrmMzGoQOyDIFIz4GvTw+j--"

alphabet = "NaRvJT1B/m6AOXL9VDFIbUGkC+sSnzh5jxQ273d4lHPg0wcEpYqruWyfZoM8itKe"

reverse_alphabet = {}

for index,char in enumerate(alphabet):
  reverse_alphabet[char] = index

def decoded(c):
    result = b""

    # Proses ciphertext per 4 karakter
    for i in range(0, len(c), 4):
        block = c[i:i+4]

        padding = block.count("-")
        values = []

        for char in block.rstrip("-"):
            values.append(reverse_alphabet[char])

        while len(values) < 4:
            values.append(0)

        combined = (
            (values[0] << 18) |
            (values[1] << 12) |
            (values[2] << 6) |
            values[3]
        )

        byte1 = (combined >> 16) & 0xFF
        byte2 = (combined >> 8) & 0xFF
        byte3 = combined & 0xFF

        if padding == 0:
            result += bytes([byte1, byte2, byte3])
        elif padding == 1:
            result += bytes([byte1, byte2])
        elif padding == 2:
            result += bytes([byte1])

    return result


current = c

for i in range(1, 5): 
  current = decoded(current).decode("ascii")
  
  print(f"[{i}/5]: {current}")