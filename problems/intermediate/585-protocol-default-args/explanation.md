Writing `func send(_ m: String, urgent: Bool = false)` in a protocol is an error (*default argument not permitted in a protocol method*). The extension overload is the standard workaround.
