import { useEffect, useRef, useState } from 'react'
import type { BookChapter } from '../../../shared/api'
import { Markdown } from './Markdown'

/** Offline reader for The Swift Programming Language (vendored from swiftlang/swift-book). */
export function BookView({ initialPath }: { initialPath?: string }): React.JSX.Element {
  const [chapters, setChapters] = useState<BookChapter[]>([])
  const [path, setPath] = useState(initialPath ?? 'GuidedTour/GuidedTour')
  const [text, setText] = useState('')
  const body = useRef<HTMLDivElement>(null)

  useEffect(() => {
    void window.judge.listBook().then(setChapters)
  }, [])
  useEffect(() => {
    if (initialPath) setPath(initialPath)
  }, [initialPath])
  useEffect(() => {
    void window.judge.getBookChapter(path).then((t) => {
      setText(t)
      body.current?.scrollTo(0, 0)
    })
  }, [path])

  const sections = [...new Set(chapters.map((c) => c.path.split('/')[0]))]
  return (
    <div className="book">
      <aside className="sidebar book-toc">
        {chapters.length === 0 && <div className="empty small">Run <code>npm run vendor-docs</code> to download the book.</div>}
        {sections.map((s) => (
          <section key={s}>
            <h3>{s.replace(/([a-z])([A-Z])/g, '$1 $2')}</h3>
            {chapters
              .filter((c) => c.path.startsWith(s + '/'))
              .map((c) => (
                <button key={c.path} className={`problem-item ${c.path === path ? 'selected' : ''}`} onClick={() => setPath(c.path)}>
                  <span className="title">{c.title}</span>
                </button>
              ))}
          </section>
        ))}
        <div className="muted small book-credit">
          The Swift Programming Language · © Apple Inc. and the Swift project authors · Apache-2.0
        </div>
      </aside>
      <div className="book-body" ref={body}>
        <Markdown source={text} />
      </div>
    </div>
  )
}
