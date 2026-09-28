import Editor, { type EditorProps, type OnMount } from '@monaco-editor/react'
import { useEffect, useRef } from 'react'

type Props = Omit<EditorProps, 'value' | 'defaultValue' | 'onChange'> & {
  /** The document text. Changes that the editor itself produced are ignored (see below). */
  value: string
  onChange: (value: string) => void
}

/**
 * A Monaco editor that never fights the person typing.
 *
 * @monaco-editor/react's controlled `value` compares the prop with the editor's text after each
 * React render and, if they differ, replaces the whole document. When keys arrive faster than React
 * re-renders (a slow machine, or a heavy re-render such as the live Markdown preview), the prop is a
 * few keystrokes behind the editor, so that replacement silently deletes what was just typed and
 * moves the cursor. Here the editor is uncontrolled: `value` is applied only when it didn't come from
 * the editor itself (loading a page, Reset, a cloud sync).
 */
export function SafeEditor({ value, onChange, onMount, options, ...rest }: Props): React.JSX.Element {
  const editorRef = useRef<Parameters<OnMount>[0]>(undefined)
  /** The last text the editor reported through onChange (or that we pushed into it). */
  const current = useRef(value)

  useEffect(() => {
    const ed = editorRef.current
    if (!ed || value === current.current) return // our own echo: never overwrite newer keystrokes
    current.current = value
    const model = ed.getModel()
    if (!model || model.getValue() === value) return
    ed.pushUndoStop()
    ed.executeEdits('external', [{ range: model.getFullModelRange(), text: value }])
    ed.pushUndoStop()
  }, [value])

  return (
    <Editor
      {...rest}
      // Monaco's newer EditContext keyboard path drops keystrokes under load in Electron (VS Code
      // made it a setting for "can't type" reports); the classic hidden-textarea input doesn't.
      options={{ ...options, editContext: false }}
      defaultValue={value}
      onMount={(ed, monaco) => {
        editorRef.current = ed
        if (ed.getValue() !== current.current) ed.setValue(current.current)
        onMount?.(ed, monaco)
      }}
      onChange={(v) => {
        current.current = v ?? ''
        onChange(v ?? '')
      }}
    />
  )
}
