From your notes. Declare `enum PasswordError: Error { case short, obvious }`. Throw `.short` if fewer than 5 characters, `.obvious` if the password is `"12345"` or `"password"`, return `"OK"` if under 10 characters, otherwise `"Good"`.

 The judge calls `try checkPassword(...)` — a thrown error shows up as `{"$error": "<case>"}`.
