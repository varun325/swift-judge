Build a `Result` pipeline without `do`/`catch`:
 1. `parse(_:) -> Result<Int, PipelineError>` — `.notANumber` if not an integer
 2. `.flatMap(validate)` — `.negative` if < 0
 3. `.map { $0 * $0 }`
 4. `.mapError { … }` — no, keep errors; finally `switch` to `"ok <value>"` / `"error <case>"`.
