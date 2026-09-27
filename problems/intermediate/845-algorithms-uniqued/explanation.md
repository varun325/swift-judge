The key projection only needs to be `Hashable`, not the element itself — so you can dedupe structs by an ID without making the whole struct Hashable.
