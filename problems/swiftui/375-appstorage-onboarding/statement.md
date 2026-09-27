Swiftful's *Manage user onboarding with @AppStorage*. Use `AppStorage(wrappedValue:_:store:)` with a **private** `UserDefaults(suiteName:)` so tests don't touch real settings. Keys: `"onboardingStep"` (Int, default 0) and `"userName"` (String, default "").

 Each inner array is one app launch: actions `next` (step += 1, max 3), `name <n>`, `skip` (step = 3). At the start of each launch, log `"launch step <s> name <n|->"` — showing values **persisted** from previous launches. Clear the suite first.
