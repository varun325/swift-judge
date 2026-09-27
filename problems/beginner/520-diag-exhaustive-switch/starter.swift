enum Weather { case sun, rain, wind, snow }
let forecast = Weather.snow

switch forecast {
case .sun: print("A nice day")
default: print("Should be okay")
}
