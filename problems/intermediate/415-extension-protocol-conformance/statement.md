Declare `protocol Summarizable { var summary: String { get } }`. **Retroactively** conform `Int` (`"int(<n>)"`), `String` (`"str(<count>)"`) and `Array where Element: Summarizable` (`"[<summaries joined by ,>]"`) in extensions.

 Return `[ints.summary, words.summary, flags-as-Int.summary]` where each Bool maps to `1`/`0` first.
