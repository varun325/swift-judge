import AppKit

func snapshotOps(_ ops: [String]) -> [String] {
    var snapshot = NSDiffableDataSourceSnapshot<String, String>()
    var reloaded: Set<String> = []
    for op in ops {
        let p = op.split(separator: " ").map(String.init)
        switch (p.first ?? "", p.count) {
        case ("section", 2): snapshot.appendSections([p[1]])
        case ("add", 3):
            if snapshot.sectionIdentifiers.contains(p[1]) {
                snapshot.appendItems(p[2].split(separator: ",").map(String.init).filter { snapshot.indexOfItem($0) == nil }, toSection: p[1])
            }
        case ("delete", 2): if snapshot.indexOfItem(p[1]) != nil { snapshot.deleteItems([p[1]]); reloaded.remove(p[1]) }
        case ("move", 4) where p[2] == "after":
            if snapshot.indexOfItem(p[1]) != nil, snapshot.indexOfItem(p[3]) != nil, p[1] != p[3] {
                snapshot.moveItem(p[1], afterItem: p[3])
            }
        case ("reload", 2): if snapshot.indexOfItem(p[1]) != nil { snapshot.reloadItems([p[1]]); reloaded.insert(p[1]) }
        default: break
        }
    }
    let sections = snapshot.sectionIdentifiers.map { "\($0): \(snapshot.itemIdentifiers(inSection: $0).joined(separator: ","))" }
    return sections + ["items \(snapshot.numberOfItems)", "reloaded \(reloaded.sorted().joined(separator: ","))"]
}
