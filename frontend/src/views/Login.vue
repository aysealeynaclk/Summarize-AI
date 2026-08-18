<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '../api/client'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const auth = useAuthStore()

const usernameOrEmail = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

async function handleSubmit() {
  error.value = ''
  loading.value = true
  try {
    const { data } = await apiClient.post('/auth/login', {
      username_or_email: usernameOrEmail.value,
      password: password.value,
    })
    auth.setSession(data.access_token, data.role)
    router.push({ name: 'home' })
  } catch (err) {
    error.value = err.response?.data?.detail || 'Giriş yapılamadı, lütfen tekrar deneyin.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-50 via-white to-slate-100 px-4">
    <div class="w-full max-w-sm bg-white rounded-2xl shadow-xl p-8 border border-slate-100">
      <h1 class="text-2xl font-bold text-center text-indigo-600 mb-1">Summarize-AI</h1>
      <p class="text-center text-sm text-slate-500 mb-6">Hesabına giriş yap</p>

      <form @submit.prevent="handleSubmit" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-slate-700 mb-1">Kullanıcı adı / E-posta</label>
          <input
            v-model="usernameOrEmail"
            type="text"
            required
            class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-slate-700 mb-1">Şifre</label>
          <input
            v-model="password"
            type="password"
            required
            class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>

        <p v-if="error" class="text-sm text-red-600 bg-red-50 border border-red-100 rounded-lg px-3 py-2">
          {{ error }}
        </p>

        <button
          type="submit"
          :disabled="loading"
          class="w-full bg-indigo-600 hover:bg-indigo-700 disabled:opacity-60 text-white font-medium py-2.5 rounded-lg transition"
        >
          {{ loading ? 'Giriş yapılıyor...' : 'Giriş Yap' }}
        </button>
      </form>

      <p class="text-center text-sm text-slate-500 mt-6">
        Hesabın yok mu?
        <router-link to="/register" class="text-indigo-600 font-medium hover:underline">Kayıt Ol</router-link>
      </p>
    </div>
  </div>
</template>
