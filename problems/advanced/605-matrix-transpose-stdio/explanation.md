`rows.first?.count` is `nil` for empty input, so `if let` handles "nothing to print". Building each output line with `map` + `joined` avoids trailing spaces.
