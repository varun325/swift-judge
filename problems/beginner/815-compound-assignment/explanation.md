`+=`, `-=`, `*=`, `/=` modify in place — and `+=` works on `String` too. Integer `/` truncates toward zero, and dividing by zero traps, hence the guard.
