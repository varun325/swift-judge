final class CopyCounter { var copies = 0 }

struct COWArray {
    init(counter: CopyCounter) {}
    mutating func append(_ x: Int) {}
    var items: [Int] { [] }
}
