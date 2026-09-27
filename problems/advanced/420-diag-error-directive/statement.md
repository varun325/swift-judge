Use `#error("Set API_KEY before building")` so that the build **fails with your own message** unless a compilation condition `HAS_KEY` is defined. You pass when the compiler emits your error text.
