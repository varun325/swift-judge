Convert an **integer** Celsius value to Fahrenheit: `F = C × 9 / 5 + 32`.

 Careful: `celsius * 9 / 5` in integer arithmetic truncates — convert first.

 ```swift
 celsiusToFahrenheit(100)  // 212.0
 celsiusToFahrenheit(37)   // 98.6
 ```
