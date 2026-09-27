final class Singer { var name = "Taylor" }

func referenceDemo(_ renames: [String]) -> [String] {
    let original = Singer()
    let alias = original
    for name in renames { alias.name = name }
    let clone = Singer()
    clone.name = original.name
    return [original.name, "\(original === alias)", "\(clone === original)"]
}
