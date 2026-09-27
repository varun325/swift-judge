Magnification is **relative to the start of the gesture**, so you multiply by the last committed scale and only commit on `.onEnded`. Forgetting that split is the classic "zoom jumps back" bug.
