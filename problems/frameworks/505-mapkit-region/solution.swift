import MapKit

func regionFor(_ points: [[Double]], padding: Double) -> [Double] {
    guard !points.isEmpty else { return [] }
    let lats = points.map { $0[0] }, lons = points.map { $0[1] }
    let center = CLLocationCoordinate2D(latitude: (lats.min()! + lats.max()!) / 2, longitude: (lons.min()! + lons.max()!) / 2)
    let span = MKCoordinateSpan(
        latitudeDelta: max((lats.max()! - lats.min()!) * padding, 0.01),
        longitudeDelta: max((lons.max()! - lons.min()!) * padding, 0.01)
    )
    let region = MKCoordinateRegion(center: center, span: span)
    return [region.center.latitude, region.center.longitude, region.span.latitudeDelta, region.span.longitudeDelta]
        .map { ($0 * 10_000).rounded() / 10_000 }
}
