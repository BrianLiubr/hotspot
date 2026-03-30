export type SourceItem = {
  id: number
  name: string
  type: string
  enabled: boolean
  base_url?: string | null
}

export type NewsItem = {
  title: string
  summary?: string | null
  source: string
  published_at?: string | null
  url: string
  rank_score?: number | null
  category?: string | null
  collected_at: string
}

export type HotnewsResponse = {
  date: string
  count: number
  items: NewsItem[]
}

export type CollectSourceResult = {
  source: string
  status: string
  item_count: number
  error_message?: string | null
}

export type CollectResponse = {
  status: string
  collected_sources: string[]
  total_items: number
  requested_sources: string[]
  success_count: number
  failed_count: number
  results: CollectSourceResult[]
  message?: string | null
}
