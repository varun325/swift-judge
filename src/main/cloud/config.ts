import { existsSync, readFileSync } from 'node:fs'

/** The public Firebase web config (not a secret: access is enforced by Firestore security rules). */
export interface FirebaseConfig {
  apiKey: string
  projectId: string
  authDomain?: string
}

/**
 * First usable config among the candidate files. Missing, empty ({}) or malformed files mean
 * "no cloud": the app then works fully offline and hides sign-in.
 */
export function loadFirebaseConfig(candidates: string[]): FirebaseConfig | undefined {
  for (const file of candidates) {
    if (!file || !existsSync(file)) continue
    try {
      const c = JSON.parse(readFileSync(file, 'utf8')) as Partial<FirebaseConfig>
      if (typeof c.apiKey === 'string' && c.apiKey && typeof c.projectId === 'string' && c.projectId) {
        return { apiKey: c.apiKey, projectId: c.projectId, authDomain: c.authDomain }
      }
    } catch {
      /* ignore a malformed file and keep looking */
    }
  }
  return undefined
}
