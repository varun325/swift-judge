import CoreLocation

func nearest(from: [Double], places: [[String]]) -> [String] {
    let me = CLLocation(latitude: from[0], longitude: from[1])
    return places
        .compactMap { p -> (String, Double)? in
            guard let lat = Double(p[1]), let lon = Double(p[2]), abs(lat) <= 90, abs(lon) <= 180 else { return nil }
            return (p[0], CLLocation(latitude: lat, longitude: lon).distance(from: me))
        }
        .sorted { $0.1 < $1.1 }
        .map { "\($0.0) \((($0.1 / 1000) * 10).rounded() / 10) km" }
}
