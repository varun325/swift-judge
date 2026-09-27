enum HTTPVersion: String {
    case `1.1` = "HTTP/1.1"
    case `2` = "HTTP/2"
}

func `formats a price with currency symbol`() -> String { "$4.99" }
let `class` = "keywords always needed backticks"

print(HTTPVersion.`2`.rawValue, HTTPVersion.`1.1`)
print(`formats a price with currency symbol`())
print(`class`)
