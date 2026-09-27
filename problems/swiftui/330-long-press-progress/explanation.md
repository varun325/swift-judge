`LongPressGesture(minimumDuration:)` gives `onPressingChanged` and `onEnded`; the progress bar is just state animated over the duration. Guarding `required > 0` avoids dividing by zero.
