<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '../api/client'

const router = useRouter()

const usernameOrEmail = ref('')
const password = ref('')
const error = ref('')
const success = ref(false)
const loading = ref(false)

async function handleSubmit() {
  error.value = ''
  loading.value = true
  try {
    await apiClient.post('/auth/register', {
      username_or_email: usernameOrEmail.value,
      password: password.value,
    })
    success.value = true
    setTimeout(() => router.push({ name: 'login' }), 2500)
  } catch (err) {
    error.value = err.response?.data?.detail || 'Kayıt oluşturulamadı, lütfen tekrar deneyin.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-50 via-white to-slate-100 px-4">
    <div class="w-full max-w-sm bg-white rounded-2xl shadow-xl p-8 border border-slate-100">
      <h1 class="text-2xl font-bold text-center text-indigo-600 mb-1">Summarize-AI</h1>
      <p class="text-center text-sm text-slate-500 mb-6">Yeni hesap oluştur</p>

      <div v-if="success" class="text-center space-y-3">
        <p class="text-sm text-green-700 bg-green-50 border border-green-100 rounded-lg px-3 py-3">
          Kaydın alındı! Hesabın, bir yönetici onayladıktan sonra aktif olacak.
        </p>
        <p class="text-xs text-slate-400">Giriş sayfasına yönlendiriliyorsun...</p>
      </div>

      <form v-else @submit.prevent="handleSubmit" class="space-y-4">
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
            minlength="6"
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
          {{ loading ? 'Kaydediliyor...' : 'Kayıt Ol' }}
        </button>
      </form>

      <p class="text-center text-sm text-slate-500 mt-6">
        Zaten hesabın var mı?
        <router-link to="/login" class="text-indigo-600 font-medium hover:underline">Giriş Yap</router-link>
      </p>
    </div>
  </div>
</template>
