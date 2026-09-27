Writing an `init` inside the struct body **removes** the synthesised memberwise initialiser. Putting custom inits in an **extension** keeps both — a well-known Swift idiom.
