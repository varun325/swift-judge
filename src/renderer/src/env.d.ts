/// <reference types="vite/client" />
import type { JudgeApi } from '../../shared/api'

declare global {
  interface Window {
    judge: JudgeApi
  }
}
