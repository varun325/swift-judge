Paul's *ScrollView effects using visualEffect()*. For a sticky header of height `h` and scroll offset `y` (negative = pulled down):
 - **stretch**: when `y < 0`, height = `h − y`, else `h`
 - **parallax**: the image moves at half speed: `offsetY = max(y, 0) / 2`
 - **fade**: opacity = `1 − min(max(y, 0) / h, 1)`

 Return `[height, offsetY, opacity]` rounded to 2 decimals per offset.
