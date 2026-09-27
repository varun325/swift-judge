The classic two-pointer merge. `a[i...]` is empty when `i == a.count`, so appending the leftovers needs no extra checks. `<=` keeps the merge **stable**.
