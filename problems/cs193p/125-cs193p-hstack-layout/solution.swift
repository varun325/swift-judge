func layoutWidths(available: Double, children: [[Double]]) -> [Double] {
    var widths = children.map { $0[0] }
    var leftover = max(0, available - widths.reduce(0, +))
    let priorities = Set(children.map { $0[2] }).sorted(by: >)
    for priority in priorities {
        var group = children.indices.filter { children[$0][2] == priority }
        group.sort { (children[$0][1] - children[$0][0]) < (children[$1][1] - children[$1][0]) }
        for (k, i) in group.enumerated() {
            let offer = leftover / Double(group.count - k)
            let extra = min(offer, children[i][1] - children[i][0])
            widths[i] += extra
            leftover -= extra
        }
    }
    return widths.map { ($0 * 100).rounded() / 100 }
}
