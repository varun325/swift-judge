func courseOrder(_ numCourses: Int, _ prerequisites: [[Int]]) -> [Int] {
    var indegree = Array(repeating: 0, count: numCourses)
    var next = Array(repeating: [Int](), count: numCourses)
    for p in prerequisites {
        next[p[1]].append(p[0])
        indegree[p[0]] += 1
    }
    var available = Set((0..<numCourses).filter { indegree[$0] == 0 })
    var order: [Int] = []
    while let course = available.min() {
        available.remove(course)
        order.append(course)
        for n in next[course] {
            indegree[n] -= 1
            if indegree[n] == 0 { available.insert(n) }
        }
    }
    return order.count == numCourses ? order : []
}
