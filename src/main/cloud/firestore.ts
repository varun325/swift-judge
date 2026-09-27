import type { FirebaseConfig } from './config'

type Fetch = typeof fetch

/** One synced record as stored in Firestore: users/{uid}/{collection}/{id}. */
export interface CloudDoc {
  id: string
  /** JSON-encoded value (one string field keeps documents schema-free and rule-checkable). */
  data: string
  /** When the value last changed on the writing machine (client clock; merge tie-breaks only). */
  updatedAt: number
  deleted?: boolean
}

export type Collection = 'problems' | 'quiz' | 'playground'

export interface CloudStore {
  /** Documents changed since `since` (server time, ISO), or all of them; plus the query's read time. */
  changed(uid: string, token: string, collection: Collection, since?: string): Promise<{ docs: CloudDoc[]; readTime?: string }>
  write(uid: string, token: string, collection: Collection, docs: CloudDoc[]): Promise<void>
}

export class CloudError extends Error {
  constructor(
    readonly status: number,
    message: string
  ) {
    super(message)
  }
}

function explain(status: number, body: string): string {
  if (status === 403) return 'Firestore refused access — deploy the security rules in firestore.rules (see README).'
  if (status === 404 && /database .* does not exist|NOT_FOUND/i.test(body)) return 'This Firebase project has no Firestore database yet (Console → Firestore Database → Create database).'
  if (status === 429) return 'Firebase free-tier quota reached for today; sync resumes tomorrow.'
  if (status === 401) return 'Your session expired — sign in again.'
  return `Firestore error ${status}`
}

/** Firestore over REST: per-user collections, server timestamps, batched commits. */
export class FirestoreRest implements CloudStore {
  constructor(
    private readonly config: FirebaseConfig,
    private readonly http: Fetch = fetch
  ) {}

  private get root(): string {
    return `projects/${this.config.projectId}/databases/(default)/documents`
  }

  private async call(url: string, token: string, body: unknown): Promise<unknown> {
    let res: Response
    try {
      res = await this.http(url, {
        method: 'POST',
        headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      })
    } catch {
      throw new CloudError(0, 'Offline — changes will sync when you reconnect.')
    }
    const text = await res.text()
    if (!res.ok) throw new CloudError(res.status, explain(res.status, text))
    return text ? JSON.parse(text) : {}
  }

  async changed(uid: string, token: string, collection: Collection, since?: string): Promise<{ docs: CloudDoc[]; readTime?: string }> {
    const docs: CloudDoc[] = []
    let readTime: string | undefined
    let cursor: unknown
    // Page through results ordered by server time so large first syncs stay within request limits.
    for (;;) {
      const structuredQuery: Record<string, unknown> = {
        from: [{ collectionId: collection }],
        orderBy: [{ field: { fieldPath: 'syncedAt' } }, { field: { fieldPath: '__name__' } }],
        limit: 300
      }
      if (since) structuredQuery.where = { fieldFilter: { field: { fieldPath: 'syncedAt' }, op: 'GREATER_THAN', value: { timestampValue: since } } }
      if (cursor) structuredQuery.startAt = { values: cursor, before: false }
      const rows = (await this.call(`https://firestore.googleapis.com/v1/${this.root}/users/${uid}:runQuery`, token, { structuredQuery })) as {
        document?: { name: string; fields: Record<string, { stringValue?: string; integerValue?: string; booleanValue?: boolean; timestampValue?: string }> }
        readTime?: string
      }[]
      let last: { name: string; syncedAt?: string } | undefined
      for (const row of rows) {
        readTime = row.readTime ?? readTime
        const d = row.document
        if (!d) continue
        const f = d.fields ?? {}
        docs.push({
          id: decodeURIComponent(d.name.split('/').pop()!),
          data: f.data?.stringValue ?? 'null',
          updatedAt: Number(f.updatedAt?.integerValue ?? 0),
          deleted: f.deleted?.booleanValue === true ? true : undefined
        })
        last = { name: d.name, syncedAt: f.syncedAt?.timestampValue }
      }
      if (rows.filter((r) => r.document).length < 300 || !last?.syncedAt) break
      cursor = [{ timestampValue: last.syncedAt }, { referenceValue: last.name }]
    }
    return { docs, readTime }
  }

  async write(uid: string, token: string, collection: Collection, docs: CloudDoc[]): Promise<void> {
    // A commit takes at most 500 writes.
    for (let i = 0; i < docs.length; i += 400) {
      const writes = docs.slice(i, i + 400).map((d) => ({
        update: {
          name: `${this.root}/users/${uid}/${collection}/${encodeURIComponent(d.id)}`,
          fields: {
            data: { stringValue: d.data },
            updatedAt: { integerValue: String(Math.round(d.updatedAt)) },
            ...(d.deleted ? { deleted: { booleanValue: true } } : {})
          }
        },
        // Server time, so incremental pulls never depend on anyone's clock.
        updateTransforms: [{ fieldPath: 'syncedAt', setToServerValue: 'REQUEST_TIME' }]
      }))
      await this.call(`https://firestore.googleapis.com/v1/${this.root}:commit`, token, { writes })
    }
  }
}
