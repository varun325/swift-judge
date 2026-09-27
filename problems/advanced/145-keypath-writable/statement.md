`struct Profile { var name = "anon"; var age = 0; var city = "?" }`. Write a generic `func update<T, V>(_ value: inout T, _ keyPath: WritableKeyPath<T, V>, to newValue: V)`.

 Updates look like `"name=Ana"`, `"age=31"`, `"city=Porto"` (ignore unknown fields or bad ages). Apply them in order, then return `[name, "\(age)", city]` read via a `[PartialKeyPath<Profile>]` array — `[\.name, \.age, \.city]`.
