import Foundation

final class Entry {
    let value: String
    init(_ value: String) { self.value = value }
}

final class DataCache {
    private let cache = NSCache<NSString, Entry>()
    init(countLimit: Int) { cache.countLimit = countLimit }
    func put(_ value: String, for key: String) { cache.setObject(Entry(value), forKey: key as NSString) }
    func get(_ key: String) -> String? { cache.object(forKey: key as NSString)?.value }
    func remove(_ key: String) { cache.removeObject(forKey: key as NSString) }
    func clear() { cache.removeAllObjects() }
}

func cacheRun(countLimit: Int, ops: [String]) -> [String] {
    let cache = DataCache(countLimit: countLimit)
    var log: [String] = []
    for op in ops {
        let p = op.split(separator: " ").map(String.init)
        switch p[0] {
        case "put" where p.count == 3: cache.put(p[2], for: p[1])
        case "get" where p.count == 2: log.append(cache.get(p[1]) ?? "miss")
        case "remove" where p.count == 2: cache.remove(p[1])
        case "clear": cache.clear()
        default: break
        }
    }
    return log
}
