import { request } from './client'
import { clearTokens, setTokens } from '../utils/storage'

export async function login(username, password) {
  const data = await request('/api/auth/login/', {
    method: 'POST',
    body: { username, password },
  })

  setTokens(data.access, data.refresh)
  return data
}

export function logout() {
  clearTokens()
}
