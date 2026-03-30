import type { CollectResponse, HotnewsResponse, SourceItem } from '../lib/types'

const API_BASE = import.meta.env.VITE_API_BASE || '/api'

async function requestJson<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(init?.headers ?? {}),
    },
    ...init,
  })

  if (!response.ok) {
    const text = await response.text()
    throw new Error(text || `Request failed: ${response.status}`)
  }

  return response.json() as Promise<T>
}

export function getApiBase() {
  return API_BASE
}

export function fetchSources() {
  return requestJson<SourceItem[]>('/v1/sources')
}

export function fetchHotnews(params: { date: string; limit: number; source?: string }) {
  const search = new URLSearchParams({
    date: params.date,
    limit: String(params.limit),
  })

  if (params.source) {
    search.set('source', params.source)
  }

  return requestJson<HotnewsResponse>(`/v1/hotnews?${search.toString()}`)
}

export function collectHotnews(source?: string) {
  const payload = source ? { source_names: [source] } : {}
  return requestJson<CollectResponse>('/v1/collect', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}
