# Playground: typing lost and duplicate `-conflict` pages (fixed in 0.2.1)

**Reported:** "Sometimes the editor in the Playground isn't working, I can't type in the Markdown notes, and it's creating duplicate files a lot."
**Affected:** 0.2.0 (duplicates need cloud sync to be signed in). Typing loss affected every version, and both editors.

## Evidence

- Cloud data for the reporting account showed `compass-diag-let-reassign-conflict`, `-2`, `-3` and `-4`
  created 30–60 s apart while that single page was being edited on one machine. No other machine was
  editing it.
- The UI test typed three bursts of text into the notes editor. Characters vanished (`" third-burst"` became `" irbut"`)
  even with no sync involved. The active element was Monaco's EditContext `<div>`.
- Experiment: the old code with only `editContext: false` kept every keystroke in 6 of 6 runs.
- Live test against the real Firebase project, using the old sync engine: 4 edit→sync cycles made 4 phantom conflict copies,
  and a deleted page came back.

## Root causes

1. **Keystrokes dropped by Monaco's EditContext input (primary cause of "can't type").** This Monaco version
   reads keyboard input through Chromium's new EditContext API by default. Under load in Electron it
   drops or reorders characters. VS Code had "can't type in the editor" reports after switching to it.
2. **Sync treated its own uploads as edits from another machine (the duplicates).** Pulls deliberately
   re-read the previous 60 s, so a write can't slip between two pulls. That re-delivers the page this
   machine uploaded a moment ago. The Playground merge only asked whether the cloud copy differed from
   the local page and whether the page had unsynced edits. It never asked whether the cloud copy had
   changed since the last sync. So every sync after an edit saved the previous text as
   `page-conflict-N`. The same gap let a re-delivered old copy re-create a page you had just deleted.
   The first sync tests missed it because their fake server's clock advanced two minutes per write,
   so the overlap never re-delivered anything.
3. **Contributing: the page reloaded on every sync notice, and the editor was React-controlled.** Each
   phantom conflict told the view "Playground changed", and the view reloaded the open page while you
   worked. Separately, `@monaco-editor/react`'s controlled `value` replaces the whole document when a
   render lags behind typing. Neither lost text in our timing tests, but both can overwrite the editor
   under you. So they were removed as well.

## Fixes

- `SafeEditor` (used by the Playground and problem editors) turns off `editContext` and ignores
  React's echo of text the editor itself produced. It only replaces the document for real outside
  changes (loading a page, Reset, sync). The Markdown preview renders with `useDeferredValue`.
- `SyncEngine.applyPages` makes a three-way decision against the last-synced version. A cloud copy
  equal to it is this machine's own echo and is ignored. It takes the cloud version only if the cloud
  changed and the local page didn't. It keeps both copies only if both changed.
- The Playground reloads the open page only if its file really changed, and never within 5 s of a keystroke.

## Tests added

- `tests/sync.test.ts` "regression" suite, using a store with realistic server timestamps:
  - no conflict copies from repeated edit→sync cycles;
  - a deleted page stays deleted;
  - a genuine concurrent edit still makes exactly one copy.

  It fails on the old engine and passes on the fix.
- `scripts/e2e.mjs`: typing in the notes editor survives a sync notice (text intact and focus kept).
- `scripts/cloud-smoke.ts`: the same regressions against a real Firebase project (4 phantom conflicts before the fix, 0 after).
