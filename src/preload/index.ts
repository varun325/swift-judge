import { contextBridge, ipcRenderer } from 'electron'
import type { JudgeApi } from '../shared/api'

const call = (channel: string) => (...args: unknown[]) => ipcRenderer.invoke(channel, ...args)

const api: JudgeApi = {
  platform: process.platform,
  listProblems: call('listProblems') as JudgeApi['listProblems'],
  getProblem: call('getProblem') as JudgeApi['getProblem'],
  run: call('run') as JudgeApi['run'],
  submit: call('submit') as JudgeApi['submit'],
  saveDraft: call('saveDraft') as JudgeApi['saveDraft'],
  resetDraft: call('resetDraft') as JudgeApi['resetDraft'],
  revealSolution: call('revealSolution') as JudgeApi['revealSolution'],
  revealHint: call('revealHint') as JudgeApi['revealHint'],
  getProgress: call('getProgress') as JudgeApi['getProgress'],
  getLearn: call('getLearn') as JudgeApi['getLearn'],
  listBook: call('listBook') as JudgeApi['listBook'],
  getBookChapter: call('getBookChapter') as JudgeApi['getBookChapter'],
  listConcepts: call('listConcepts') as JudgeApi['listConcepts'],
  listQuiz: call('listQuiz') as JudgeApi['listQuiz'],
  saveQuizAnswer: call('saveQuizAnswer') as JudgeApi['saveQuizAnswer'],
  getQuizProgress: call('getQuizProgress') as JudgeApi['getQuizProgress'],
  swiftInfo: call('swiftInfo') as JudgeApi['swiftInfo'],
  openExternal: call('openExternal') as JudgeApi['openExternal'],
  cloud: {
    status: call('cloud:status') as JudgeApi['cloud']['status'],
    signIn: call('cloud:signIn') as JudgeApi['cloud']['signIn'],
    resetPassword: call('cloud:resetPassword') as JudgeApi['cloud']['resetPassword'],
    signOut: call('cloud:signOut') as JudgeApi['cloud']['signOut'],
    syncNow: call('cloud:syncNow') as JudgeApi['cloud']['syncNow'],
    onChange: (cb) => {
      const listener = (_e: unknown, status: Parameters<typeof cb>[0], dataChanged: boolean): void => cb(status, dataChanged)
      ipcRenderer.on('cloud:changed', listener)
      return () => ipcRenderer.removeListener('cloud:changed', listener)
    }
  },
  playground: {
    root: call('pg:root') as JudgeApi['playground']['root'],
    list: call('pg:list') as JudgeApi['playground']['list'],
    load: call('pg:load') as JudgeApi['playground']['load'],
    save: call('pg:save') as JudgeApi['playground']['save'],
    create: call('pg:create') as JudgeApi['playground']['create'],
    ensure: call('pg:ensure') as JudgeApi['playground']['ensure'],
    rename: call('pg:rename') as JudgeApi['playground']['rename'],
    remove: call('pg:remove') as JudgeApi['playground']['remove'],
    reveal: call('pg:reveal') as JudgeApi['playground']['reveal'],
    run: call('pg:run') as JudgeApi['playground']['run']
  },
  onProblemsChanged: (cb) => {
    const listener = (): void => cb()
    ipcRenderer.on('problemsChanged', listener)
    return () => ipcRenderer.removeListener('problemsChanged', listener)
  }
}

contextBridge.exposeInMainWorld('judge', api)
