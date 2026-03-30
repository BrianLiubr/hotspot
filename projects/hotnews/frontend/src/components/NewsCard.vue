<script setup lang="ts">
import type { NewsItem } from '../lib/types'

defineProps<{
  item: NewsItem
  formatDateTime: (value?: string | null) => string
}>()
</script>

<template>
  <article class="panel news-card">
    <div class="news-top">
      <div>
        <div class="chip-row">
          <span class="chip">{{ item.source }}</span>
          <span v-if="item.category" class="chip subtle">{{ item.category }}</span>
        </div>
        <h2>
          <a :href="item.url" target="_blank" rel="noreferrer">{{ item.title }}</a>
        </h2>
      </div>
      <div class="score" v-if="item.rank_score !== null && item.rank_score !== undefined">
        {{ item.rank_score }}
      </div>
    </div>

    <p class="summary">{{ item.summary || '暂无摘要' }}</p>

    <dl class="meta-grid">
      <div>
        <dt>发布时间</dt>
        <dd>{{ formatDateTime(item.published_at) }}</dd>
      </div>
      <div>
        <dt>采集时间</dt>
        <dd>{{ formatDateTime(item.collected_at) }}</dd>
      </div>
    </dl>
  </article>
</template>
