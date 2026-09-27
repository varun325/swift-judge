Model `enum Shape { case circle(radius: Double); case rectangle(width: Double, height: Double); case triangle(base: Double, height: Double) }` with an `area` computed property.

 Parse each spec — `"circle 2"`, `"rectangle 3 4"`, `"triangle 6 2"` — into a `Shape` (skip malformed specs) and return the total area. Use `Double.pi`.
