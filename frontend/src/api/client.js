import { clearTokens, getAccessToken, getRefreshToken, setTokens } from '../utils/storage'

const API_BASE = 'http://127.0.0.1:8000'

export async function request(path, { method = 'GET', body, auth = false } = {}) {
  let accessToken = auth ? getAccessToken() : ''

  async function doFetch(token = accessToken) {
    const headers = { 'Content-Type': 'application/json' }
    if (auth && token) {
      headers.Authorization = `Bearer ${token}`
    }

    const response = await fetch(`${API_BASE}${path}`, {
      method,
      headers,
      body: body ? JSON.stringify(body) : undefined,
    })

    const data = await response.json().catch(() => ({}))
    return { response, data }
  }

  let { response, data } = await doFetch()

  if (auth && response.status === 401) {
    const refresh = getRefreshToken()
    if (refresh) {
      const refreshResult = await fetch(`${API_BASE}/api/auth/refresh/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh }),
      })
      const refreshData = await refreshResult.json().catch(() => ({}))

      if (refreshResult.ok && refreshData.access) {
        setTokens(refreshData.access, refresh)
        accessToken = refreshData.access
        ;({ response, data } = await doFetch(accessToken))
      } else {
        clearTokens()
      }
    }
  }

  if (!response.ok) {
    const msg = data.error || data.detail || 'Request failed'
    throw new Error(msg)
  }

  return data
}
