Compare how many times a view that shows only `name` would be invalidated:
 - **Legacy**: `final class ProfileVM: ObservableObject { @Published var name; @Published var followers }` — any `@Published` change fires `objectWillChange` (count via `sink`).
 - **Modern**: `@Observable final class ProfileModel { var name; var followers }` — only reads of `name` are tracked (re-arm after each fire).

 Apply changes `name <v>` / `followers <n>` to both and return `[legacyCount, modernCount]`.
