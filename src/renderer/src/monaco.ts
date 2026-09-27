import { loader } from '@monaco-editor/react'
import * as monaco from 'monaco-editor/editor/editor.api'
import 'monaco-editor/languages/definitions/swift/register'
import 'monaco-editor/languages/definitions/markdown/register'
import EditorWorker from 'monaco-editor/editor/editor.worker?worker'

// Bundle Monaco locally (no CDN) so the app works offline.
self.MonacoEnvironment = { getWorker: () => new EditorWorker() }
loader.config({ monaco })

monaco.editor.defineTheme('judge-dark', {
  base: 'vs-dark',
  inherit: true,
  rules: [
    { token: 'keyword', foreground: 'FC5FA3' },
    { token: 'string', foreground: 'FC6A5D' },
    { token: 'number', foreground: 'D0BF69' },
    { token: 'comment', foreground: '6C7986' },
    { token: 'type.identifier', foreground: '5DD8FF' }
  ],
  colors: { 'editor.background': '#1f2025', 'editor.lineHighlightBackground': '#2a2c33' }
})

export { monaco }

// Exposed for the e2e driver (scripts/e2e) to set editor contents without keyboard auto-closing.
;(window as unknown as { monaco: typeof monaco }).monaco = monaco
