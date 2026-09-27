/** Platform-specific labels (macOS vs Windows/Linux). */
export const isMac = window.judge.platform === 'darwin'
export const RUN_KEY = isMac ? '⌘↵' : 'Ctrl+Enter'
export const SUBMIT_KEY = isMac ? '⌘⇧↵' : 'Ctrl+Shift+Enter'
export const FILE_MANAGER = isMac ? 'Finder' : window.judge.platform === 'win32' ? 'Explorer' : 'file manager'
