A legacy API sends prices **either** as numbers or as strings (`"price": "9.99"` or `9.99`), may omit `tags` (default `[]`), and nests the name: `{"info": {"name": "Pen"}}`.

 Write `struct Product: Decodable` with `name: String`, `priceCents: Int` (rounded), `tags: [String]`, implementing `init(from decoder:)` with a **nested container**. Return `"<name> <cents> [tags joined by ,]"` per product, or `["error: <DecodingError case name>"]` on failure (`"keyNotFound"`, `"typeMismatch"`, `"dataCorrupted"`, `"valueNotFound"`).
