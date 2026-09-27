Sean Allen's *Dead Simple Formatting*. For each value return `"<USD> | <EUR in de_DE> | <percent> | <compact>"` using `.formatted(...)` with **explicit locales** (never rely on the device locale in tests):
 - `.currency(code: "USD").locale(en_US)`
 - `.currency(code: "EUR").locale(de_DE)`
 - `.percent.precision(.fractionLength(1)).locale(en_US)` (value interpreted as a fraction)
 - `.number.notation(.compactName).locale(en_US)`
