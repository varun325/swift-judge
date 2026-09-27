func downsample(_ images: [[Double]]) -> [String] {
    images.map { i in
        let (pw, ph, dw, dh, scale) = (i[0], i[1], i[2], i[3], i[4])
        let factor = min(1, max(dw * scale / pw, dh * scale / ph))
        let w = Int((pw * factor).rounded(.up)), h = Int((ph * factor).rounded(.up))
        let decoded = w * h * 4 / 1024
        let original = Int(pw) * Int(ph) * 4 / 1024
        return "\(w)x\(h)px, \(decoded) KB vs \(original) KB"
    }
}
