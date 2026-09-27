`defer` blocks run in **reverse** order when the scope exits — including when it exits by throwing, *before* control reaches the `catch`. `try?` swallows the error into `nil`.
