`fallthrough` runs the **next** case's body without checking its pattern — so `-5` also gets `"small"` and `20` also gets `"other"`. Without `fallthrough`, exactly one case runs.
