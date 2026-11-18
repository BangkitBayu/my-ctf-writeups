# Detecting NoSQL Injection

> **Lab Description:** The product category filter for this lab is powered by a MongoDB NoSQL database. It is vulnerable to NoSQL injection. To solve the lab, perform a NoSQL injection attack that causes the application to display unreleased products.

## Lab Overview

| Property             | Detail                                                                                                     |
| :------------------- | :--------------------------------------------------------------------------------------------------------- |
| **Category**         | No SQL Injection                                                                                           |
| **Difficulty Level** | Apprentice                                                                                                 |
| **Lab URL**          | [PortSwigger Lab Link](https://portswigger.net/web-security/nosql-injection/lab-nosql-injection-detection) |
| **Status**           | In progress                                                                                                |
| **Date Completed**   |                                                                                                            |

## Analysis

Diberikan web sebagai berikut:

![1](./lab-01-img/Screenshot_2026-11-18_08-39-55.png)

Objektif dalam lab ini yaitu melakukan `No SQL Injection` terhadap fitur filter kategori produk pada web e-commerce untuk menampilkan produk yang belum rilis.

**Pertama**, saya mengamati bagaimana cara web load semua produk. Saya ambil sample pada kategori `Clothing,shoes and accessories`

```text
GET /filter?category=Clothing%2c+shoes+and+accessories
```

Response dari server adalah halaman HTML beserta produk yang memenuhi kategori tersebut.

**Kedua**, Uji coba query yang memicu `No SQL Injection`

## Exploitation

## New Knowledge

## References

- [Explained NoSQL Injection by Portswigger](https://portswigger.net/web-security/nosql-injection)

- [OWASP WSTG No SQL Injection](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/07-Injection/05.6-NoSQL_Injection/)
