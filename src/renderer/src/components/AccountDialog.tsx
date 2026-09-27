import { useState } from 'react'
import type { CloudStatus } from '../../../shared/api'

function ago(ms?: number): string {
  if (!ms) return 'not yet'
  const s = Math.round((Date.now() - ms) / 1000)
  if (s < 10) return 'just now'
  if (s < 60) return `${s} s ago`
  if (s < 3600) return `${Math.round(s / 60)} min ago`
  return new Date(ms).toLocaleString()
}

export function statusLine(status: CloudStatus): string {
  if (!status.signedIn) return 'Not signed in: progress stays on this machine.'
  if (status.state === 'syncing') return 'Syncing…'
  if (status.state === 'offline') return 'Offline: changes will sync when you reconnect.'
  if (status.state === 'error') return status.error ?? 'Sync failed.'
  return `Synced ${ago(status.lastSync)}`
}

interface Props {
  status: CloudStatus
  onClose: () => void
}

/** Sign in / create account / reset password, or (signed in) sync status and sign out. */
export function AccountDialog({ status, onClose }: Props): React.JSX.Element {
  const [email, setEmail] = useState(status.email ?? '')
  const [password, setPassword] = useState('')
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState<string>()
  const [info, setInfo] = useState<string>()

  const act = async (fn: () => Promise<unknown>, done?: string): Promise<void> => {
    setBusy(true)
    setError(undefined)
    setInfo(undefined)
    try {
      await fn()
      if (done) setInfo(done)
    } catch (e) {
      setError(String((e as Error).message ?? e).replace(/^Error invoking remote method '[^']+': (\w*Error: )?/, ''))
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal account-dialog" role="dialog" aria-label="Account" onClick={(e) => e.stopPropagation()}>
        <header>
          <h2>☁ {status.signedIn ? 'Account & sync' : 'Sign in to sync'}</h2>
          <button className="close" onClick={onClose} aria-label="Close">×</button>
        </header>
        {status.signedIn ? (
          <>
            <p>
              Signed in as <strong>{status.email}</strong>
            </p>
            <p className={`sync-line ${status.state}`}>{statusLine(status)}</p>
            {status.conflicts && (
              <p className="muted small">
                Edited on two machines at once, so both versions were kept: {status.conflicts.join(', ')}
              </p>
            )}
            <p className="muted small">
              Solved problems, attempts, hints, revisit schedule, code drafts, quiz answers and Playground pages
              sync across every machine you sign in on.
            </p>
            {error && <p className="form-error">{error}</p>}
            <div className="account-actions">
              <button className="run" disabled={busy} onClick={() => void act(() => window.judge.cloud.syncNow())}>
                Sync now
              </button>
              <button className="ghost" disabled={busy} onClick={() => void act(() => window.judge.cloud.signOut())}>
                Sign out
              </button>
            </div>
          </>
        ) : (
          <form
            className="account-form"
            onSubmit={(e) => {
              e.preventDefault()
              void act(() => window.judge.cloud.signIn(email, password, false))
            }}
          >
            <p className="muted small">
              Keep your progress, code drafts, quiz answers and Playground notes in sync across your machines.
            </p>
            <label>
              Email
              <input type="email" autoComplete="email" autoFocus required value={email} onChange={(e) => setEmail(e.target.value)} />
            </label>
            <label>
              Password
              <input type="password" autoComplete="current-password" required minLength={6} value={password} onChange={(e) => setPassword(e.target.value)} />
            </label>
            {error && <p className="form-error">{error}</p>}
            {info && <p className="form-info">{info}</p>}
            <div className="account-actions">
              <button type="submit" className="run" disabled={busy}>
                {busy ? 'Working…' : 'Sign in'}
              </button>
              <button type="button" className="ghost" disabled={busy} onClick={() => void act(() => window.judge.cloud.signIn(email, password, true))}>
                Create account
              </button>
              <button
                type="button"
                className="link"
                disabled={busy || !email}
                onClick={() => void act(() => window.judge.cloud.resetPassword(email), `Password reset email sent to ${email}.`)}
              >
                Forgot password?
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  )
}
