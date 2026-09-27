struct FeedModel {
    let pageSize: Int
    let totalAvailable: Int
    private(set) var loadedCount: Int
    private(set) var page = 0
    private(set) var isLoading = false
    var hasMore: Bool { loadedCount < totalAvailable }

    init(pageSize: Int, totalAvailable: Int) {
        self.pageSize = pageSize
        self.totalAvailable = totalAvailable
        loadedCount = min(pageSize, totalAvailable)
    }

    mutating func rowAppeared(_ index: Int) -> Int? {
        guard hasMore, !isLoading, index >= loadedCount - 3 else { return nil }
        isLoading = true
        page += 1
        loadedCount = min(loadedCount + pageSize, totalAvailable)
        isLoading = false
        return page
    }
}

func feedPaging(pageSize: Int, totalAvailable: Int, visibleIndices: [Int]) -> [String] {
    var model = FeedModel(pageSize: pageSize, totalAvailable: totalAvailable)
    return visibleIndices.map { i in model.rowAppeared(i).map { "load page \($0)" } ?? "-" }
}
