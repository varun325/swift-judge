Tuple assignment swaps without a temporary (the law of exclusivity prevents `swap(&m[i][j], &m[j][i])` on the same array — try it!). `reverse()` mutates in place, `reversed()` returns a view.
