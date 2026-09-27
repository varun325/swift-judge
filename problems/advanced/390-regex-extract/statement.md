Find every date written `YYYY-MM-DD` in the text using a Swift **regex literal** with named or positional captures, and reformat each as `DD/MM/YYYY`. Only accept months 01–12 and days 01–31 (check numerically after matching).

 ```swift
 extractDates("Due 2024-03-15, moved to 2024-13-01 then 2025-01-02.")
 // ["15/03/2024", "02/01/2025"]
 ```
