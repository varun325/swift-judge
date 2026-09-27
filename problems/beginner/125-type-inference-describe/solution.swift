func inferredTypes() -> [String] {
    [
        String(describing: type(of: 42)),
        String(describing: type(of: 3.0)),
        String(describing: type(of: "hi")),
        String(describing: type(of: true)),
        String(describing: type(of: [1, 2])),
        String(describing: type(of: ["a": 1])),
        String(describing: type(of: (1, "x"))),
        String(describing: type(of: 1...3)),
    ]
}
