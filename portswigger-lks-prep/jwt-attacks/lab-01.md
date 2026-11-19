# JWT authentication bypass via unverified signature

> **Lab Description:**  This lab uses a JWT-based mechanism for handling sessions. Due to implementation flaws, the server doesn't verify the signature of any JWTs that it receives. To solve the lab, modify your session token to gain access to the admin panel at `/admin`, then delete the user `carlos`. You can log in to your own account using the following credentials: `wiener:peter`
>  
## Lab Overview

| Property             | Detail                                                                                                     |
| :------------------- | :--------------------------------------------------------------------------------------------------------- |
| **Category**         |  JWT Attacks                                                                                          |
| **Difficulty Level** | Apprentice                                                                                                 |
| **Lab URL**          | [PortSwigger Lab Link](https://portswigger.net/web-security/jwt/lab-jwt-authentication-bypass-via-unverified-signature) |
| **Status**           | In  progress                                                                                                |
| **Date Completed**   |                                                                                                           |

## Analysis

## Exploitation

### Final Exploit

## New Knowledge

## References
- [Working with JWTs in Burp Suite](https://portswigger.net/burp/documentation/desktop/testing-workflow/vulnerabilities/session-management/jwts)
- [JWT attacks](https://portswigger.net/web-security/jwt)
- [JWT WSTG](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/06-Session_Management/10-JSON_Web_Tokens/)
