#if HAS_KEY
let apiKey = "secret"
#else
#error("Set API_KEY before building")
#endif
