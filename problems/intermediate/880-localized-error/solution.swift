import Foundation

enum UploadError: LocalizedError {
    case emptyFile
    case tooLarge(limitMB: Int)
    case offline

    var errorDescription: String? {
        switch self {
        case .emptyFile: "The file is empty."
        case .tooLarge(let limit): "The file is larger than \(limit) MB."
        case .offline: "You're offline."
        }
    }

    var recoverySuggestion: String? {
        switch self {
        case .emptyFile: "Choose a different file."
        case .tooLarge: "Compress the file and try again."
        case .offline: "Check your connection."
        }
    }
}

func upload(sizeMB: Int) throws -> String {
    if sizeMB < 0 { throw UploadError.offline }
    if sizeMB == 0 { throw UploadError.emptyFile }
    if sizeMB > 25 { throw UploadError.tooLarge(limitMB: 25) }
    return "uploaded \(sizeMB)MB"
}

func uploadMessages(_ sizes: [Int]) -> [String] {
    sizes.map { size in
        do {
            return try upload(sizeMB: size)
        } catch let error as LocalizedError {
            return "\(error.localizedDescription) — \(error.recoverySuggestion ?? "")"
        } catch {
            return error.localizedDescription
        }
    }
}
