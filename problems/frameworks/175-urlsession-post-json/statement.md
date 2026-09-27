Build a `URLRequest` for `POST https://api.example.com/todos` with `Content-Type: application/json`, `Authorization: Bearer <token>`, and a JSON body encoded from `struct NewTodo: Encodable { let title: String; let done: Bool }` (`done: false`). Send it with `session.data(for:)` and decode the response `{"id": …}`.

 Return `[method, content-type header, authorization header, body as sorted-keys JSON, "id <n>"]` — the mock (given) echoes the request so you can verify it.
