Add `func myMap<T>(_ transform: (Element) throws -> T) rethrows -> [T]` to `Array`. Because it `rethrows`, calling it with a **non-throwing** closure needs no `try`.

 In `demo`: (1) uppercase every word with `myMap` **without** `try`; (2) then `try? words.myMap(parse)` where `parse` throws for words containing digits — append `"parsed"` or `"rejected"`.
