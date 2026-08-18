<script setup>
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from './stores/auth'

const router = useRouter()
const auth = useAuthStore()
const { locale, t } = useI18n()

function handleLogout() {
  auth.logout()
  router.push({ name: 'login' })
}

function setLocale(value) {
  locale.value = value
  localStorage.setItem('locale', value)
}
</script>

<template>
  <div class="min-h-screen flex flex-col">
    <nav class="bg-white border-b border-slate-200 px-6 py-4 flex items-center justify-between shadow-sm">
      <div class="flex items-center gap-6">
        <span class="font-semibold text-lg text-indigo-600">{{ t('nav.brand') }}</span>
        <template v-if="auth.isAuthenticated">
          <router-link
            to="/"
            class="text-sm text-slate-600 hover:text-indigo-600 transition"
            active-class="text-indigo-600 font-medium"
          >
            {{ t('nav.home') }}
          </router-link>
          <template v-if="auth.isAdmin">
            <router-link
              to="/admin/logs"
              class="text-sm text-slate-600 hover:text-indigo-600 transition"
              active-class="text-indigo-600 font-medium"
            >
              {{ t('nav.logs') }}
            </router-link>
            <router-link
              to="/admin/users"
              class="text-sm text-slate-600 hover:text-indigo-600 transition"
              active-class="text-indigo-600 font-medium"
            >
              {{ t('nav.users') }}
            </router-link>
          </template>
        </template>
      </div>

      <div class="flex items-center gap-4">
        <div class="flex items-center border border-slate-200 rounded-full p-0.5 text-xs font-medium">
          <button
            @click="setLocale('tr')"
            :class="[
              'px-2.5 py-1 rounded-full transition',
              locale === 'tr' ? 'bg-indigo-600 text-white' : 'text-slate-500 hover:text-slate-700',
            ]"
          >
            TR
          </button>
          <button
            @click="setLocale('en')"
            :class="[
              'px-2.5 py-1 rounded-full transition',
              locale === 'en' ? 'bg-indigo-600 text-white' : 'text-slate-500 hover:text-slate-700',
            ]"
          >
            EN
          </button>
        </div>

        <button
          v-if="auth.isAuthenticated"
          @click="handleLogout"
          class="text-sm px-3 py-1.5 rounded-md border border-slate-300 text-slate-600 hover:bg-slate-100 transition"
        >
          {{ t('nav.logout') }}
        </button>
      </div>
    </nav>

    <main class="flex-1">
      <router-view />
    </main>
  </div>
</template>
