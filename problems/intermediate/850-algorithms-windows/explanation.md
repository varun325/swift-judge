Slices (`SubSequence`) share storage with the original, so windows are cheap. `zip(self, dropFirst())` is the classic way to pair each element with its successor.
