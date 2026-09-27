Swift has no `abstract` keyword. Model a "template method": `protocol Report` requires `var title: String` and `func rows() -> [String]`, and a protocol extension provides `func render() -> [String]` returning `["== <title> ==", rows…, "(<n> rows)"]`.

 `SalesReport(amounts)` titles itself `"Sales"` with rows `"$<amount>"`; `TeamReport(headcounts)` titles `"Team"` with rows `"team <i>: <count>"` (1-based). `sizes[0]` feeds sales, `sizes[1]` team. Return both renders concatenated.
