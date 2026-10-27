# XOR Properties

### Category 
Cryptography

### Description
> In the last challenge, you saw how XOR worked at the level of bits. In this one, we're going to cover the properties of the XOR operation and then use them to undo a chain of operations that have > encrypted a flag. Gaining an intuition for how this works will help greatly when you come to attacking real cryptosystems later, especially in the block ciphers category.
There are four main properties we should consider when we solve challenges using the XOR operator
- Commutative: A ⊕ B = B ⊕ A
- Associative: A ⊕ (B ⊕ C) = (A ⊕ B) ⊕ C
- Identity: A ⊕ 0 = A
- Self-Inverse: A ⊕ A = 0
>Let's break this down. Commutative means that the order of the XOR operations is not important. Associative means that a chain of operations can be carried out without order (we do not need to worry about brackets). The identity is 0, so XOR with 0 "does nothing", and lastly something XOR'd with itself returns zero.
Let's put this into practice! Below is a series of outputs where three random keys have been XOR'd together and with the flag. Use the above properties to undo the encryption in the final line to obtain the flag.
- KEY1 = a6c8b6733c9b22de7bc0253266a3867df55acde8635e19c73313
- KEY2 ^ KEY1 = 37dcb292030faa90d07eec17e3b1c6d8daf94c35d4c9191a5e1e
- KEY2 ^ KEY3 = c1545756687e7573db23aa1c3452a098b71a7fbf0fddddde5fc1
- FLAG ^ KEY1 ^ KEY3 ^ KEY2 = 04ee9855208a2cd59091d04767ae47963170d1660df7f56f5faf 

### Source
[xor_properties](https://cryptohack.org/courses/intro/xor1/).

### Solution
Saya selesaikan dengan solver berikut

```python
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
```
### References
- [https://www.geeksforgeeks.org/python/get-the-logical-xor-of-two-variables-in-python/](https://www.geeksforgeeks.org/python/get-the-logical-xor-of-two-variables-in-python/)
- [https://en.wikipedia.org/wiki/Exclusive_or](https://en.wikipedia.org/wiki/Exclusive_or)
