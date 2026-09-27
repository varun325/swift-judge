#if HAS_KEY
let apiKey = "secret"
#else
// fail the build with a helpful message
let apiKey = ""
#endif
