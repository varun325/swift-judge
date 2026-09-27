Swift 5.9 added **parameter packs**: generics over a variable number of types. Write:
 - `func describeAll<each T>(_ value: repeat each T) -> [String]` returning `String(describing:)` for every argument
 - `func allNonNil<each T>(_ value: repeat (each T)?) -> Bool`

 Return `describeAll(1, "two", 3.0, true)` + `["\(allNonNil(1, "a", 2.5))", "\(allNonNil(1, nil as String?))"]`.
