protocol ButtonTextProtocol { var buttonText: String { get } }
protocol ButtonPressedProtocol { func buttonPressed() -> String }
typealias ButtonDataSourceProtocol = ButtonTextProtocol & ButtonPressedProtocol

struct DefaultDataSource: ButtonDataSourceProtocol {
    var buttonText: String { "Protocols are awesome!" }
    func buttonPressed() -> String { "default pressed" }
}

struct AlternativeDataSource: ButtonDataSourceProtocol {
    var buttonText: String { "Protocols are lame." }
    func buttonPressed() -> String { "alternative pressed" }
}

struct ScreenModel {
    let dataSource: any ButtonDataSourceProtocol
    func render() -> String { "\(dataSource.buttonText) | \(dataSource.buttonPressed())" }
}

func screens(_ sources: [String]) -> [String] {
    sources.map { name in
        let source: any ButtonDataSourceProtocol = name == "alternative" ? AlternativeDataSource() : DefaultDataSource()
        return ScreenModel(dataSource: source).render()
    }
}
