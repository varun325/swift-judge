`phrases[$0, default: …]` and `phrases[$0] ?? …` are equivalent for reads. The `default:` subscript shines for **writes** like `counts[k, default: 0] += 1`.
