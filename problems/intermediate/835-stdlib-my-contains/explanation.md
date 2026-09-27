The `Equatable` version only exists where `==` does — a constrained extension. Returning early on the first match gives short-circuiting, just like the real `contains`.
