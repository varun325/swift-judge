Your notes' Bug 5: `default` on your own enum hides new cases. Prove the safety net exists: declare `enum Weather { case sun, rain, wind, snow }`, then write a `switch` over a `Weather` value that handles **sun, rain and wind only**, with **no `default`**.

 You pass when the compiler refuses because the switch isn't exhaustive.
