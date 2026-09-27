import { contextBridge, ipcRenderer } from 'electron'
import type { JudgeApi } from '../shared/api'

const call = (channel: string) => (...args: unknown[]) => ipcRenderer.invoke(channel, ...args)

const api: JudgeApi = {
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
  onProblemsChanged: (cb) => {
    const listener = (): void => cb()
    ipcRenderer.on('problemsChanged', listener)
    return () => ipcRenderer.removeListener('problemsChanged', listener)
  }
}

contextBridge.exposeInMainWorld('judge', api)
