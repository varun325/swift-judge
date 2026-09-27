import Dispatch

let queue = DispatchQueue(label: "serial")
var log: [String] = []
queue.async { log.append("A") }
queue.async { log.append("B") }
queue.sync { log.append("C") }
log.append("D")
queue.async { log.append("E") }
queue.sync { }
print(log.joined(separator: ","))
