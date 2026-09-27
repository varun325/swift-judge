Model: `Company` has an optional `ceo: Person?`; `Person` has an optional `address: Address?`; `Address` has `city: String`. Each record is `[companyName, ceoName, city]` where `"-"` means *missing* (a missing CEO name means no CEO; a missing city means the CEO has no address).

 Build the models, then return `company.ceo?.address?.city.count` for each.
