import api from './client'

export const sendChat = (message, context = {}) =>
  api.post('/copilot/chat', { message, context })
