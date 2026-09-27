Search each array in its own child task (`withTaskGroup(of: Int?.self)`); a task returns its **array index** if it contains `target`. Return the **smallest** matching index found, or `-1`.

 When any task finds a match, call `group.cancelAll()`. Inside the search loop, check `Task.isCancelled` so remaining work stops early — but because you want the *smallest* index, only cancel tasks with a larger index… (simplify: keep collecting all results and take the minimum; cancellation just speeds things up).
