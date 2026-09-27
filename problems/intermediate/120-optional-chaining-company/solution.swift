struct Address { let city: String }
struct Person { let name: String; let address: Address? }
struct Company { let name: String; let ceo: Person? }

func ceoCityLengths(_ records: [[String]]) -> [Int?] {
    records.map { r in
        let address = r[2] == "-" ? nil : Address(city: r[2])
        let ceo = r[1] == "-" ? nil : Person(name: r[1], address: address)
        let company = Company(name: r[0], ceo: ceo)
        return company.ceo?.address?.city.count
    }
}
