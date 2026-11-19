# JWT authentication bypass via unverified signature

> **Lab Description:** This lab uses a JWT-based mechanism for handling sessions. Due to implementation flaws, the server doesn't verify the signature of any JWTs that it receives. To solve the lab, modify your session token to gain access to the admin panel at `/admin`, then delete the user `carlos`. You can log in to your own account using the following credentials: `wiener:peter`

## Lab Overview

| Property             | Detail                                                                                                                  |
| :------------------- | :---------------------------------------------------------------------------------------------------------------------- |
| **Category**         | JWT Attacks                                                                                                             |
| **Difficulty Level** | Apprentice                                                                                                              |
| **Lab URL**          | [PortSwigger Lab Link](https://portswigger.net/web-security/jwt/lab-jwt-authentication-bypass-via-unverified-signature) |
| **Status**           | In progress                                                                                                             |
| **Date Completed**   |                                                                                                                         |

## Analysis

Diberikan web sebagai berikut:

![1](./lab-01-imgs/Screenshot_2026-11-19_08-35-42.png)

Objektif lab ini adalah kita diminta untuk bypass auth dengan memanfaatkan token JWT yang signature nya tidak diverifikasi, sehingga kita bisa memodifikasi session token yang diberikan di admin panel dan menghapus user `carlos`.

**Pertama**, saya login menggunakan akun `wiener:peter`

![2](./lab-01-imgs/Screenshot_2026-11-19_08-49-14.png)

Setelah berhasil login, kita akan diberi sebuah token JWT yang diset pada session cookie, berikut potongan Header Request

```text
GET /my-account?id=wiener HTTP/2
Host: 0aef00da031cf7ac815f0cc000bb00f8.web-security-academy.net
Cookie: session=eyJraWQiOiI1YTRkOWE0YS04MzgxLTQxNTYtOTM0OC1jMmIyMGYwMGE0ZWEiLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJwb3J0c3dpZ2dlciIsImV4cCI6MTc5NTA1NjY0MSwic3ViIjoid2llbmVyIn0.tg67xF2Ox62p0IyeKNShit_ZGxgK3gWlSIEEdOS0ZeCNN9FnhLSNyJqCiMXQK7NGT9-99A6y2ZVHu8pD14fm04wDqQyx4c8jx00bSYEDP7fWA9YjbzyrxgQh_qrsXvcXeqh8RLgxkfWMHe9-d82OqHzaASE7HAOgqxN58nMljWnnzIWilvn8cfDhgBScLjtJXSpIcUQTOaEqOY-sFGl7GIazCQ-9TciRDeD_GbiJqRrGVaQj2e7jg4y-qqTG0FtePD9UFcHIpz3YE_cz_7SQ5kivu02vqUqGnzRG0RsmQji8CtT-oufMthUGVV0YK8uzaGPPWWIXlVtIkMzEGY_DFw
```

**Kedua**, Periksa Token JWT

![3](./lab-01-imgs/Screenshot_2026-11-19_09-00-58.png)

Pada header JWT, JWT tersebut digenerate menggunakan alg `RS256`

**Ketiga** Modifikasi payload JWT & Signature, disini saya ubah `sub` payload yang dimiliki oleh `wiener` saya ubah menjadi carlos

![4](./lab-01-imgs/Screenshot_2026-11-19_09-06-30.png)

Sebelum saya Sign ulang terlebih dahulu saya buat key baru menggunakan ekstensi `JWT Editor` burp suite, karena algortima dari token tersebut adalah `RS256` maka saya generate new RSA key

![5](./lab-01-imgs/Screenshot_2026-11-19_09-26-49.png)

![6](./lab-01-imgs/Screenshot_2026-11-19_09-27-08.png)

![7](./lab-01-imgs/Screenshot_2026-11-19_09-27-51.png)

Setelah itu masukkan token yang baru dibuat dengan sign ulang

![8](./lab-01-imgs/Screenshot_2026-11-19_09-32-32.png)

Lalu send request ke browser dengan `follow redirection` dan periksa response nya
![9](./lab-01-imgs/Screenshot_2026-11-19_09-33-28.png)

## Exploitation

**Pertama** Minta request ke admin panel pada `/admin`, teruskan permintaan ke burp repeater dan modifikasi payload JWT, ubah `sub` ke `administrator`

![10](./lab-01-imgs/Screenshot_2026-11-19_09-56-28.png)

Sign ulang dan masukkan key RSA yang sudah dibuat, lalu request ke original browser, jika berhasil kita akan masuk ke dashboard `admin`

![11](./lab-01-imgs/Screenshot_2026-11-19_09-58-35.png)

**Kedua** Hapus akun `carlos`

![12](./lab-01-imgs/Screenshot_2026-11-19_10-01-26.png)

> **NOTE** : ketika request ke `/admin` atau akun tetap login sebagai `wiener`, intercept request nya dan sign ulang keynya seperti langkah pertama.

## New Knowledge

- Mempelajari struktur dan cara kerja JWT sebagai session token

## References

- [Working with JWTs in Burp Suite](https://portswigger.net/burp/documentation/desktop/testing-workflow/vulnerabilities/session-management/jwts)
- [JWT attacks](https://portswigger.net/web-security/jwt)
- [JWT WSTG](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/06-Session_Management/10-JSON_Web_Tokens/)
