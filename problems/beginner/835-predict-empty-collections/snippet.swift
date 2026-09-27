var scores = [String: Int]()
var names = [String]()
var ids = Set<Int>()
var more = Array<Int>()
scores["ana"] = 3
names.append("bo")
ids.insert(7); ids.insert(7)
more += [1, 2]
print(scores, names, ids, more)
print(scores.isEmpty, names.count, ids.count, more.isEmpty)
print([Int]() == [], [String: Int]().count)
