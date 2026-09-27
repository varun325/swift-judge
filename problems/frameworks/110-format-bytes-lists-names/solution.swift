import Foundation

func describeUpload(files: [String], sizes: [Int], fullName: [String]) -> [String] {
    let us = Locale(identifier: "en_US")
    var name = PersonNameComponents()
    name.givenName = fullName.first
    name.familyName = fullName.count > 1 ? fullName[1] : nil
    return [
        files.formatted(.list(type: .and).locale(us)),
        Int64(sizes.reduce(0, +)).formatted(.byteCount(style: .file).locale(us)),
        name.formatted(.name(style: .abbreviated).locale(us)),
    ]
}
