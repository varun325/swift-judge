`try?` turns "throws or returns T" into `T?`, discarding the error — handy when you only care whether it worked. `Int.min / -1` is the one integer division that overflows.
