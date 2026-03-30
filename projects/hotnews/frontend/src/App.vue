<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'

import NewsCard from './components/NewsCard.vue'
import { collectHotnews, fetchHotnews, fetchSources, getApiBase } from './api/hotnews'
import type { NewsItem, SourceItem } from './lib/types'

const sources = ref<SourceItem[]>([])
const news = ref<NewsItem[]>([])
const loading = ref(false)
const collecting = ref(false)
const error = ref('')
const collectMessage = ref('')
const currentDate = ref(defaultYesterday())
const selectedSource = ref('')
const limit = ref(20)
const count = ref(0)

function defaultYesterday() {
  const now = new Date()
  now.setDate(now.getDate() - 1)
  return now.toISOString().slice(0, 10)
}

function formatDateTime(value?: string | null) {
  if (!value) return '—'
  return new Intl.DateTimeFormat('zh-CN', {
    dateStyle: 'medium',
    timeStyle: 'short',
  }).format(new Date(value))
}

async function loadSources() {
  sources.value = await fetchSources()
}

async function loadHotnews() {
  loading.value = true
  error.value = ''
  try {
    const data = await fetchHotnews({
      date: currentDate.value,
      limit: limit.value,
      source: selectedSource.value || undefined,
    })
    news.value = data.items
    count.value = data.count
  } catch (err) {
    error.value = err instanceof Error ? err.message : '加载失败'
  } finally {
    loading.value = false
  }
}

async function collectNow() {
  collecting.value = true
  error.value = ''
  collectMessage.value = ''
  try {
    const data = await collectHotnews(selectedSource.value || undefined)
    collectMessage.value = `${data.message ?? '采集完成'}：成功 ${data.success_count} 个源，新增/更新 ${data.total_items} 条。`
    await loadHotnews()
  } catch (err) {
    error.value = err instanceof Error ? err.message : '采集失败'
  } finally {
    collecting.value = false
  }
}

const activeSourceLabel = computed(() => selectedSource.value || '全部来源')
const apiBase = getApiBase()

onMounted(async () => {
  await loadSources()
  await loadHotnews()
})
</script>

<template>
  <div class="page-shell">
    <header class="hero">
      <div>
        <p class="eyebrow">Hotnews Dashboard</p>
        <h1>热点聚合看板</h1>
        <p class="subtext">前后端分离版：FastAPI + Vue3，支持筛选、采集和 Docker 部署。</p>
      </div>
      <button class="primary-btn" :disabled="collecting" @click="collectNow">
        {{ collecting ? '采集中…' : '立即采集' }}
      </button>
    </header>

    <section class="panel filters">
      <div class="field">
        <label for="date">日期</label>
        <input id="date" v-model="currentDate" type="date" />
      </div>

      <div class="field">
        <label for="source">来源</label>
        <select id="source" v-model="selectedSource">
          <option value="">全部来源</option>
          <option v-for="source in sources" :key="source.id" :value="source.name">
            {{ source.name }}
          </option>
        </select>
      </div>

      <div class="field small">
        <label for="limit">数量</label>
        <input id="limit" v-model="limit" type="number" min="1" max="100" />
      </div>

      <div class="actions">
        <button class="secondary-btn" :disabled="loading" @click="loadHotnews">
          {{ loading ? '刷新中…' : '刷新列表' }}
        </button>
      </div>
    </section>

    <section class="stats-row">
      <div class="stat-card">
        <span class="stat-label">当前筛选</span>
        <strong>{{ activeSourceLabel }}</strong>
      </div>
      <div class="stat-card">
        <span class="stat-label">结果数</span>
        <strong>{{ count }}</strong>
      </div>
      <div class="stat-card">
        <span class="stat-label">API Base</span>
        <strong>{{ apiBase }}</strong>
      </div>
    </section>

    <p v-if="collectMessage" class="notice success">{{ collectMessage }}</p>
    <p v-if="error" class="notice error">{{ error }}</p>

    <section class="news-list">
      <NewsCard
        v-for="item in news"
        :key="`${item.source}-${item.url}`"
        :item="item"
        :format-date-time="formatDateTime"
      />

      <div v-if="!loading && news.length === 0" class="panel empty-state">当前条件下暂无数据。</div>
    </section>
  </div>
</template>
