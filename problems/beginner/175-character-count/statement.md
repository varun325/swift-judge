Return `[characters, unicodeScalars, utf16 units, utf8 bytes]` for the string.

 ```swift
 lengths("abc")  // [3, 3, 3, 3]
 lengths("é")    // depends on how the é is encoded!
 ```
