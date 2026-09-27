Checkpoint 7: `class Animal` with `legs: Int`. Subclasses `Dog` (overrides `speak()` → `"Woof"`) with sub-subclasses `Corgi` (`"Yip"`) and `Poodle` (`"Bark bark"`); `Cat` adds `isTame: Bool` via its own initialiser (and `speak()` → `"Meow"` or `"Hiss"` when not tame), with subclasses `Persian` and `Lion` (`"Roar"`).

 Specs: `corgi`, `poodle`, `dog`, `persian`, `lion`, `wildcat` (a `Cat` with `isTame: false`). Return `"<speak()> (<legs> legs)"` for each.
