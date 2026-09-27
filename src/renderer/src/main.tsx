import { createRoot } from 'react-dom/client'
import './monaco'
import './styles.css'
import { App } from './App'

document.body.classList.add(`platform-${window.judge.platform}`)

createRoot(document.getElementById('root')!).render(<App />)
