With a `SymmetricKey` derived deterministically from a password via `HKDF<SHA256>.deriveKey(inputKeyMaterial:salt:info:outputByteCount:)`:
 1. For each message, compute an HMAC-SHA256 signature and verify it with `HMAC.isValidAuthenticationCode` — log `"sig ok"` / `"sig bad"`; the message at `tamperIndex` is modified before verification.
 2. Seal each message with `AES.GCM.seal`, then open it; log the decrypted text, or `"decrypt failed"` if the sealed box was tampered (flip one byte of the combined data at `tamperIndex`).
