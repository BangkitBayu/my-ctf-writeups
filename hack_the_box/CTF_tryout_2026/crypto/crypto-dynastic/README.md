# Crypto Dynastic

### CATEGORY 
Cryptography

### DESCRIPTION
> You find yourself trapped inside a sealed gas chamber, and suddenly, the air is pierced by the sound of a distorted voice played through a pre-recorded tape. Through this eerie transmission, you discover that within the next 15 minutes, this very chamber will be inundated with lethal hydrogen cyanide. As the tape’s message concludes, a sudden mechanical whirring fills the chamber, followed by the ominous ticking of a clock. You realise that each beat is one step closer to death. Darkness envelops you, your right hand restrained by handcuffs, and the exit door is locked. Your situation deteriorates as you realise that both the door and the handcuffs demand the same passcode to unlock. Panic is a luxury you cannot afford; swift action is imperative. As you explore your surroundings, your trembling fingers encounter a torch. Instantly, upon flipping the switch, the chamber is bathed in a dim glow, unveiling cryptic letters etched into the walls and a disturbing image of a Roman emperor drawn in blood. Decrypting the letters will provide you the key required to unlock the locks. Use the torch wisely as its battery is almost drained out!.

### Files
1. output.txt - Output dari enkripsi
2. source.py - Source code untuk mengenkripsi pesan

### Analysis
Saya sempet muter-muter dan bingung dengan soal ini, tetapi saya menemukan 'AHA' ketika saya analisa lagi source code pada soal ini bahwa pesan yang dienkripsi hanya digeser saja, insight ini saya dapatkan ketika memahami fungsi to_identity_map dan from_identity_map dimana fungsi ini digunakan untuk melakukan operasi pergeseran dari argumen yang dimasukkan, lalu fungsi encrypt digunakan untuk mengenkripsi pesan dimana nantinya jika karakter pesan itu bukan alphabet dia hanya menyimpannya, tetapi jika alphabet dia akan melakukan pergeseran. Hal ini membuat saya berpikir untuk membalik cara kerja dari fungsi enkripsi yaitu melakukan pengurangan. Tantangan ini menggunakan algoritma Chiper klasik yaitu Trimetheus Chiper.

### Exploitation

```python
#!/usr/bin/python3

ch = "DJF_CTA_SWYH_NPDKK_MBZ_QPHTIGPMZY_KRZSQE?!_ZL_CN_PGLIMCU_YU_KJODME_RYGZXL"

def to_identity_map(a):
return ord(a) - 0x41

def from_identity_map(a):
return chr(a % 26 + 0x41)

def decrypt(c):
m = ''
for i in range(len(c)):
	ch = c[i]
	if not ch.isalpha():
		dch = ch
		else:
			chi = to_identity_map(ch)
			dch = from_identity_map(chi - i)
			m += dch
			return m
			
			p = decrypt(ch)
			
			print("HTB{" + p + "}")
			
```

![run](./img/run.png)

Hola, flagnya berhasil dideskripsi:v
![flag](./img/flag.png)

### References
- [https://www.geeksforgeeks.org/python/ord-function-python/](https://www.geeksforgeeks.org/python/ord-function-python/)
- [https://www.w3schools.com/python/ref_func_chr.asp](https://www.w3schools.com/python/ref_func_chr.asp)
