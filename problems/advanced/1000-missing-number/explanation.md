XOR-ing every index and every value cancels pairs (`x ^ x == 0`), leaving the missing number — no overflow risk. The sum approach (`n(n+1)/2 − Σ`) is equally O(n) but can overflow for huge `n`.
