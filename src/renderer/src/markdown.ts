import hljs from 'highlight.js/lib/core'
import swift from 'highlight.js/lib/languages/swift'
import json from 'highlight.js/lib/languages/json'
import { Marked } from 'marked'

hljs.registerLanguage('swift', swift)
hljs.registerLanguage('json', json)

const marked = new Marked({
  gfm: true,
  renderer: {
    code({ text, lang }) {
      const language = lang && hljs.getLanguage(lang) ? lang : 'swift'
      const html = hljs.highlight(text, { language }).value
      return `<pre class="code"><code class="hljs language-${language}">${html}</code></pre>`
    },
    link({ href, text }) {
      // Links open in the system browser (main process intercepts window.open).
      return `<a href="${href}" target="_blank" rel="noreferrer">${text}</a>`
    }
  }
})

export function renderMarkdown(md: string): string {
  return marked.parse(md, { async: false })
}
