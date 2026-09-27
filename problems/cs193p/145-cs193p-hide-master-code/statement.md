L8 adds restart and warns about **animation revealing hidden state** (e.g. the master code flashing during a transition). The model decides visibility: implement `CodeBreaker` with `attempt(_:)`, `isOver` (solved or out of attempts), `restart()` and `masterDisplay` (`"????"`-style while playing; the real pegs once over). Guesses of the wrong length or already tried are rejected.

 Process guesses (`"restart"` restarts); after each, log `"<attempts> <masterDisplay> <playing|solved|lost|rejected>"`.
