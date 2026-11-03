from pwn import xor

plain = "label"

# convert plain text into ascii 
asci =  [ord(char) for char in plain]

#xor ascii
xored = xor(asci, 13)
print(xored)
