`addingReportingOverflow(_:)` returns a tuple `(partialValue, overflow)`. `&+` would silently wrap instead — useful for hashing, dangerous for money.
