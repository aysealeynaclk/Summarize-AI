<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from './stores/auth'

const router = useRouter()
const auth = useAuthStore()

function handleLogout() {
  auth.logout()
  router.push({ name: 'login' })
}
</script>

<template>
  <div class="min-h-screen flex flex-col">
    <nav v-if="auth.isAuthenticated" class="bg-white border-b border-slate-200 px-6 py-4 flex items-center justify-between shadow-sm">
      <div class="flex items-center gap-6">
        <span class="font-semibold text-lg text-indigo-600">Summarize-AI</span>
        <router-link
          to="/"
          class="text-sm text-slate-600 hover:text-indigo-600 transition"
          active-class="text-indigo-600 font-medium"
        >
          Ana Sayfa
        </router-link>
        <template v-if="auth.isAdmin">
          <router-link
            to="/admin/logs"
            class="text-sm text-slate-600 hover:text-indigo-600 transition"
            active-class="text-indigo-600 font-medium"
          >
            Loglar
          </router-link>
          <router-link
            to="/admin/users"
            class="text-sm text-slate-600 hover:text-indigo-600 transition"
            active-class="text-indigo-600 font-medium"
          >
            Kullanıcı Yönetimi
          </router-link>
        </template>
      </div>
      <button
        @click="handleLogout"
        class="text-sm px-3 py-1.5 rounded-md border border-slate-300 text-slate-600 hover:bg-slate-100 transition"
      >
        Çıkış Yap
      </button>
    </nav>

    <main class="flex-1">
      <router-view />
    </main>
  </div>
</template>
