Swift cases **don't** fall through by default (no forgotten `break` bugs). `fallthrough` opts in, jumping into the next case's body **without checking its pattern**.
