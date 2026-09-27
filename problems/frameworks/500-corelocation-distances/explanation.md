`CLLocation.distance(from:)` accounts for the Earth's curvature — never compute distances with Pythagoras on lat/lon degrees. `CLLocationCoordinate2DIsValid` does the same range check as here.
