enum Weather { case sun, rain, wind, snow }
let forecast = Weather.snow

switch forecast {
case .sun: print("A nice day")
case .rain: print("Pack an umbrella")
case .wind: print("Hold onto your hat")
}
