<script setup>
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import apiClient from '../api/client'

const { t } = useI18n()

const text = ref('')
const outputLanguage = ref('tr')
const summary = ref('')
const error = ref('')
const loading = ref(false)
const recentSummaries = ref([])

async function handleSummarize() {
  error.value = ''
  summary.value = ''
  loading.value = true
  try {
    const { data } = await apiClient.post('/summarize', {
      text: text.value,
      language: outputLanguage.value,
    })
    summary.value = data.summary
    await loadRecentSummaries()
  } catch (err) {
    error.value = err.response?.data?.detail || t('home.genericError')
  } finally {
    loading.value = false
  }
}

async function loadRecentSummaries() {
  try {
    const { data } = await apiClient.get('/summaries/me')
    recentSummaries.value = data
  } catch {
    // sessizce geç, ana akışı bozmasın
  }
}

onMounted(loadRecentSummaries)
</script>

<template>
  <div class="max-w-3xl mx-auto px-4 py-10">
    <h1 class="text-2xl font-bold text-slate-800 mb-1">{{ t('home.title') }}</h1>
    <p class="text-slate-500 mb-6">{{ t('home.subtitle') }}</p>

    <div class="bg-white rounded-2xl shadow-sm border border-slate-100 p-6 space-y-4">
      <textarea
        v-model="text"
        rows="8"
        :placeholder="t('home.placeholder')"
        class="w-full px-4 py-3 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 resize-none"
      ></textarea>

      <div class="flex items-center justify-between">
        <div class="flex items-center gap-2">
          <label class="text-xs text-slate-500">{{ t('home.outputLanguageLabel') }}</label>
          <select
            v-model="outputLanguage"
            class="text-sm px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            <option value="tr">Türkçe</option>
            <option value="en">English</option>
          </select>
        </div>

        <button
          @click="handleSummarize"
          :disabled="loading || !text.trim()"
          class="bg-indigo-600 hover:bg-indigo-700 disabled:opacity-60 text-white font-medium px-6 py-2.5 rounded-lg transition"
        >
          {{ loading ? t('home.summarizing') : t('home.summarize') }}
        </button>
      </div>

      <p v-if="error" class="text-sm text-red-600 bg-red-50 border border-red-100 rounded-lg px-3 py-2">
        {{ error }}
      </p>

      <div v-if="summary" class="bg-indigo-50 border border-indigo-100 rounded-lg px-4 py-3">
        <p class="text-xs font-medium text-indigo-500 mb-1">{{ t('home.summaryLabel') }}</p>
        <p class="text-slate-800 whitespace-pre-line">{{ summary }}</p>
      </div>
    </div>

    <div v-if="recentSummaries.length" class="mt-8">
      <h2 class="text-sm font-semibold text-slate-600 mb-3">{{ t('home.recentTitle') }}</h2>
      <ul class="space-y-3">
        <li
          v-for="log in recentSummaries"
          :key="log.id"
          class="bg-white border border-slate-100 rounded-lg px-4 py-3 shadow-sm"
        >
          <p class="text-xs text-slate-400 mb-1">
            {{ new Date(log.created_at).toLocaleString('tr-TR') }}
          </p>
          <p class="text-sm text-slate-700">{{ log.output_summary }}</p>
        </li>
      </ul>
    </div>
  </div>
</template>
