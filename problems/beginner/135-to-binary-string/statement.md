Return `value` written in the given `radix` (2…36), using lowercase letters for digits above 9, with a leading `-` for negatives. Hint: `String` has an initialiser for exactly this.

 ```swift
 format(255, radix: 16)  // "ff"
 format(5, radix: 2)     // "101"
 format(-8, radix: 8)    // "-10"
 ```
