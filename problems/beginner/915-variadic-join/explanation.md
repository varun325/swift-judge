A variadic `String...` arrives as `[String]`. Because you can't forward an array to a variadic parameter, the real work lives in an array-based overload. Default arguments can follow variadics.
