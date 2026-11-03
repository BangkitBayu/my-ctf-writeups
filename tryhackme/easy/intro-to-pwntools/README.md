# TryHackMe - Intro To PWNTools

### Category 
PWN / Binary Exploitation.

### Description
> An introductory room for the binary exploit toolkit Pwntools.


### Source
[Intro To PWNTools](https://tryhackme.com/room/introtopwntools).

## Solution
Diberikan website sebagai berikut
![1](./images/1.png)
Seperti keterangan ada di deskripsi soal, website ini tidak bisa dikunjungi dengan cara yang biasa, sehingga kita hanya bisa mengunjungi halaman utamanya saja. Namun, ada clue lain yang diberikan di soal itu yaitu Directory Enumeration, artinya kita perlu melakukan scanning pada halaman website untuk menemukan path apa saja yang ada diwebsite target ini.

**01 Recon**
Langkah awal saya melakukan Recon untuk mengumpulkan data tentang target seperti kesalahan konfigurasi dll. 
