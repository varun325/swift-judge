import { useMemo } from 'react'
import { renderMarkdown } from '../markdown'

export function Markdown({ source }: { source: string }): React.JSX.Element {
  const html = useMemo(() => renderMarkdown(source), [source])
  return <div className="markdown" dangerouslySetInnerHTML={{ __html: html }} />
}
