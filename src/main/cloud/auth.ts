import type { FirebaseConfig } from './config'

export interface Session {
  uid: string
  email: string
  refreshToken: string
}

type Fetch = typeof fetch

/** Firebase Auth error codes → messages a learner can act on. */
const MESSAGES: Record<string, string> = {
  EMAIL_EXISTS: 'An account with this email already exists — sign in instead.',
  EMAIL_NOT_FOUND: 'No account with this email.',
  INVALID_PASSWORD: 'Wrong email or password.',
  INVALID_LOGIN_CREDENTIALS: 'Wrong email or password.',
  INVALID_EMAIL: 'That email address looks invalid.',
  MISSING_PASSWORD: 'Enter a password.',
  USER_DISABLED: 'This account has been disabled.',
  TOO_MANY_ATTEMPTS_TRY_LATER: 'Too many attempts — wait a few minutes and try again.',
  OPERATION_NOT_ALLOWED: 'Email/password sign-in is not enabled for this Firebase project (Console → Authentication → Sign-in method).',
  TOKEN_EXPIRED: 'Your session expired — sign in again.',
  INVALID_REFRESH_TOKEN: 'Your session expired — sign in again.',
  USER_NOT_FOUND: 'This account no longer exists — sign in again.',
  CONFIGURATION_NOT_FOUND: 'Firebase Authentication is not set up for this project (Console → Authentication → Get started).'
}

export class AuthError extends Error {
  constructor(
    readonly code: string,
    message: string
  ) {
    super(message)
  }
}

function toAuthError(body: unknown, status: number): AuthError {
  const raw = (body as { error?: { message?: string } })?.error?.message ?? `HTTP ${status}`
  const code = raw.split(' ')[0].split(':')[0]
  if (code === 'WEAK_PASSWORD') return new AuthError(code, 'Use a password of at least 6 characters.')
  return new AuthError(code, MESSAGES[code] ?? `Sign-in failed (${raw}).`)
}

/** Email/password auth over Firebase's REST API (no SDK), with ID-token refresh. */
export class AuthClient {
  private token?: { value: string; expiresAt: number; uid: string }

  constructor(
    private readonly config: FirebaseConfig,
    private readonly http: Fetch = fetch
  ) {}

  private async post(url: string, body: Record<string, unknown>, form = false): Promise<Record<string, string>> {
    let res: Response
    try {
      res = await this.http(url, {
        method: 'POST',
        headers: { 'Content-Type': form ? 'application/x-www-form-urlencoded' : 'application/json' },
        body: form ? new URLSearchParams(body as Record<string, string>).toString() : JSON.stringify(body)
      })
    } catch {
      throw new AuthError('NETWORK', 'Can’t reach Firebase — check your internet connection.')
    }
    const json = (await res.json().catch(() => ({}))) as Record<string, string>
    if (!res.ok) throw toAuthError(json, res.status)
    return json
  }

  private endpoint(method: string): string {
    return `https://identitytoolkit.googleapis.com/v1/accounts:${method}?key=${encodeURIComponent(this.config.apiKey)}`
  }

  private remember(uid: string, idToken: string, expiresIn: string): void {
    this.token = { value: idToken, uid, expiresAt: Date.now() + (Number(expiresIn) || 3600) * 1000 }
  }

  async signUp(email: string, password: string): Promise<Session> {
    const r = await this.post(this.endpoint('signUp'), { email, password, returnSecureToken: true })
    this.remember(r.localId, r.idToken, r.expiresIn)
    return { uid: r.localId, email: r.email, refreshToken: r.refreshToken }
  }

  async signIn(email: string, password: string): Promise<Session> {
    const r = await this.post(this.endpoint('signInWithPassword'), { email, password, returnSecureToken: true })
    this.remember(r.localId, r.idToken, r.expiresIn)
    return { uid: r.localId, email: r.email, refreshToken: r.refreshToken }
  }

  async sendPasswordReset(email: string): Promise<void> {
    await this.post(this.endpoint('sendOobCode'), { requestType: 'PASSWORD_RESET', email })
  }

  /** A valid ID token for the session, refreshing it (and the refresh token) when needed. */
  async idToken(session: Session): Promise<string> {
    if (this.token && this.token.uid === session.uid && this.token.expiresAt - Date.now() > 60_000) return this.token.value
    const r = await this.post(
      `https://securetoken.googleapis.com/v1/token?key=${encodeURIComponent(this.config.apiKey)}`,
      { grant_type: 'refresh_token', refresh_token: session.refreshToken },
      true
    )
    session.refreshToken = r.refresh_token ?? session.refreshToken
    this.remember(r.user_id, r.id_token, r.expires_in)
    return r.id_token
  }

  /** Deletes the signed-in account (used by the live smoke test to clean up after itself). */
  async deleteAccount(session: Session): Promise<void> {
    await this.post(this.endpoint('delete'), { idToken: await this.idToken(session) })
  }

  forget(): void {
    this.token = undefined
  }
}
