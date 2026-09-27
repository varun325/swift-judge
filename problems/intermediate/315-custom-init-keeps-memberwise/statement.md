`struct Player { let name: String; let number: Int }`. Add `init(name: String)` that assigns `number` = the sum of the Unicode scalar values of the name's characters, modulo 100 — **in an extension**, so the free memberwise `init(name:number:)` still exists.

 `players` makes the first player with `Player(name:number: 10)` and the rest with `Player(name:)`, returning `"<name>#<number>"`.
