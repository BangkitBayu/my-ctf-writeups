# SQL injection vulnerability in WHERE clause allowing retrieval of hidden data

> **Lab Description:**  This lab contains a SQL injection vulnerability in the product category filter. When the user selects a category, the application carries out a SQL query like the following: `SELECT * FROM products WHERE category = 'Gifts' AND released = 1` To solve the lab, perform a SQL injection attack that causes the application to display one or more unreleased products.

## Lab Overview

| Property             | Detail                                                                                                     |
| :------------------- | :--------------------------------------------------------------------------------------------------------- |
| **Category**         | SQL Injection                                                                                           |
| **Difficulty Level** | Apprentice                                                                                                 |
| **Lab URL**          | [PortSwigger Lab Link](https://portswigger.net/web-security/sql-injection/lab-retrieve-hidden-data) |
| **Status**           | In progress                                                                                                |
| **Date Completed**   |                                                                                                       |

## Analysis

Diberikan web sebagai berikut:

## Exploitation

## New Knowledge

## References

- [Explained SQL Injection by Portswigger](https://portswigger.net/web-security/sql-injection#what-is-sql-injection-sqli)

- [OWASP WSTG SQL Injection](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/07-Injection/05-SQL_Injection/)
