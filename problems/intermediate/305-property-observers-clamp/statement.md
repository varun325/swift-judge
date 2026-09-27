`struct Speaker` has `var volume = 50` with:
 - `willSet`: append `"will <old>-><new>"` to `log`
 - `didSet`: clamp the stored value into `0...100`, then append `"did <final>"`

 (`log` is a `var log: [String] = []` property of the struct.) Apply every change and return the log.
