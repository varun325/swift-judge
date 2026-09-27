L4's model: `typealias Peg = String` (Color in the course) and `struct Code { var kind: Kind; var pegs: [Peg] }` with `enum Kind { case master(isHidden: Bool), guess, attempt([Match]), unknown }`. Build the board: the master (hidden until an attempt is fully exact), then each attempt with its matches (reuse your scoring from the previous problem: exact first, then inexact).

 Return one line per code: `"master:<pegs or ????>"` then `"attempt:<pegs> <e>E<i>I"`, and finally `"won"`/`"playing"`.
