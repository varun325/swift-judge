Clean a raw settings dictionary: parse values to `Int` dropping anything unparsable (`compactMapValues`), then double every value (`mapValues`), then keep keys that don't start with `"_"` (`filter`).
