import { existsSync, readFileSync, rmSync, writeFileSync } from 'node:fs'
import type { CloudStatus } from '../../shared/api'
import { AuthClient, AuthError, type Session } from './auth'
import type { FirebaseConfig } from './config'
import { CloudError, FirestoreRest } from './firestore'
import { SyncEngine, type SyncDeps, type SyncResult } from './sync'

/** Encrypts the session at rest (Electron's safeStorage: the macOS Keychain / Windows DPAPI). */
export interface SecretBox {
  available(): boolean
  encrypt(text: string): Buffer
  decrypt(data: Buffer): string
}

interface Options {
  config: FirebaseConfig | undefined
  sessionFile: string
  box: SecretBox
  deps: Omit<SyncDeps, 'store' | 'idToken'>
  /** Called when status changes or synced data changed locally. */
  notify: (status: CloudStatus, changed?: SyncResult) => void
}

const UPLOAD_DELAY_MS = 8_000
const FOCUS_MIN_GAP_MS = 60_000
const PERIODIC_MS = 5 * 60_000

/** Sign-in state + background sync scheduling for the main process. */
export class CloudService {
  private readonly auth?: AuthClient
  private readonly engine?: SyncEngine
  private session?: Session
  private status: CloudStatus
  private uploadTimer?: NodeJS.Timeout
  private periodic?: NodeJS.Timeout
  private lastSync = 0

  constructor(private readonly opts: Options) {
    this.status = { enabled: Boolean(opts.config), signedIn: false, state: 'idle' }
    if (!opts.config) return
    this.auth = new AuthClient(opts.config)
    const store = new FirestoreRest(opts.config)
    this.engine = new SyncEngine({ ...opts.deps, store, idToken: (s) => this.auth!.idToken(s) })
    this.session = this.loadSession()
    if (this.session) this.status = { ...this.status, signedIn: true, email: this.session.email }
  }

  current(): CloudStatus {
    return this.status
  }

  /** Start background syncing (call once the app is ready). */
  start(): void {
    if (!this.session) return
    void this.syncNow()
    this.periodic = setInterval(() => void this.syncNow(), PERIODIC_MS)
  }

  private set(patch: Partial<CloudStatus>, changed?: SyncResult): void {
    this.status = { ...this.status, ...patch }
    this.opts.notify(this.status, changed)
  }

  // ---- session persistence (encrypted; never stored in plain text)
  private loadSession(): Session | undefined {
    const { sessionFile, box } = this.opts
    if (!existsSync(sessionFile) || !box.available()) return undefined
    try {
      return JSON.parse(box.decrypt(readFileSync(sessionFile))) as Session
    } catch {
      rmSync(sessionFile, { force: true })
      return undefined
    }
  }

  private saveSession(): void {
    const { sessionFile, box } = this.opts
    // Without OS encryption (e.g. Linux with no keyring) the session lives in memory only.
    if (this.session && box.available()) writeFileSync(sessionFile, box.encrypt(JSON.stringify(this.session)))
  }

  // ---- account actions
  async signIn(email: string, password: string, create: boolean): Promise<CloudStatus> {
    if (!this.auth) throw new Error('Cloud sync is not configured in this build.')
    this.session = create ? await this.auth.signUp(email.trim(), password) : await this.auth.signIn(email.trim(), password)
    this.saveSession()
    this.engine!.reset() // a new sign-in merges everything once
    this.set({ signedIn: true, email: this.session.email, error: undefined })
    clearInterval(this.periodic)
    this.periodic = setInterval(() => void this.syncNow(), PERIODIC_MS)
    await this.syncNow()
    return this.status
  }

  async resetPassword(email: string): Promise<void> {
    if (!this.auth) throw new Error('Cloud sync is not configured in this build.')
    await this.auth.sendPasswordReset(email.trim())
  }

  async signOut(): Promise<CloudStatus> {
    clearTimeout(this.uploadTimer)
    clearInterval(this.periodic)
    if (this.session) await this.syncNow().catch(() => undefined) // last upload before leaving
    this.session = undefined
    this.auth?.forget()
    this.engine?.reset()
    rmSync(this.opts.sessionFile, { force: true })
    this.set({ signedIn: false, email: undefined, state: 'idle', error: undefined, lastSync: undefined })
    return this.status
  }

  // ---- sync triggers
  /** A local change happened: upload shortly (coalescing bursts such as typing). */
  changed(): void {
    if (!this.session) return
    clearTimeout(this.uploadTimer)
    this.uploadTimer = setTimeout(() => void this.syncNow(), UPLOAD_DELAY_MS)
  }

  /** The window gained focus: pick up changes made on another machine. */
  focused(): void {
    if (this.session && Date.now() - this.lastSync > FOCUS_MIN_GAP_MS) void this.syncNow()
  }

  async syncNow(): Promise<CloudStatus> {
    if (!this.session || !this.engine) return this.status
    clearTimeout(this.uploadTimer)
    this.set({ state: 'syncing' })
    try {
      const result = await this.engine.sync(this.session)
      this.saveSession() // the refresh token may have rotated
      this.lastSync = Date.now()
      this.set({ state: 'idle', lastSync: this.lastSync, error: undefined, conflicts: result.conflicts.length ? result.conflicts : undefined }, result)
    } catch (e) {
      const expired = e instanceof AuthError && ['TOKEN_EXPIRED', 'INVALID_REFRESH_TOKEN', 'USER_NOT_FOUND', 'USER_DISABLED'].includes(e.code)
      const offline = (e instanceof CloudError && e.status === 0) || (e instanceof AuthError && e.code === 'NETWORK')
      if (expired) {
        this.session = undefined
        rmSync(this.opts.sessionFile, { force: true })
        this.set({ signedIn: false, email: undefined, state: 'error', error: (e as Error).message })
      } else {
        this.set({ state: offline ? 'offline' : 'error', error: (e as Error).message })
      }
    }
    return this.status
  }

  /** Best-effort final upload when the app quits (bounded so quitting never hangs). */
  async flush(timeoutMs = 4000): Promise<void> {
    if (!this.session) return
    clearInterval(this.periodic)
    await Promise.race([this.syncNow(), new Promise((r) => setTimeout(r, timeoutMs))])
  }
}
