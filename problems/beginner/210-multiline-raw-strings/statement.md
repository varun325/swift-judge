Return the path `C:\Users\<user>\Documents` using a **raw string** (`#"..."#`) so you don't have to escape every backslash, and interpolate `user` with raw-string interpolation syntax.

 ```swift
 windowsPath(user: "varun")   // C:\Users\varun\Documents
 ```
