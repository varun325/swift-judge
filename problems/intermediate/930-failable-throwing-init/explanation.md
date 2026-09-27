A failable `init?` says *whether* construction worked; a throwing `init` also says *why*. Here the failable one reuses the throwing one via `try?` and assigns `self` (allowed for value types).
