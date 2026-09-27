L5's layout rule: a container **offers** space, each child **chooses** its size, then the container positions them — and an HStack offers space to its **least flexible** children first. Model it: each child is `[minWidth, maxWidth, priority]`.
 1. Every child first gets its `minWidth`; the leftover is `available − Σ min` (if negative, children just get their minimums).
 2. Hand out leftover by `priority` group, **highest first**. Within a group, go from least flexible (smallest `max − min`) to most; each child is offered `leftover ÷ childrenRemainingInGroup` and takes `min(offer, max − min)` extra.
 Return widths in the original order, rounded to 2 decimals.
