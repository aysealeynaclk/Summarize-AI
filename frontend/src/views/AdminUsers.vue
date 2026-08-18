<script setup>
import { ref, computed, onMounted } from 'vue'
import apiClient from '../api/client'

const users = ref([])
const error = ref('')
const loading = ref(true)
const actionError = ref('')

const showCreateForm = ref(false)
const newUser = ref({ username_or_email: '', password: '', role: 'user', status: 'active' })
const creating = ref(false)

const resetPasswordFor = ref(null)
const newPassword = ref('')

const pendingUsers = computed(() => users.value.filter((u) => u.status === 'pending'))
const otherUsers = computed(() => users.value.filter((u) => u.status !== 'pending'))

const statusLabel = {
  pending: 'Onay Bekliyor',
  active: 'Aktif',
  inactive: 'Pasif',
}

const statusStyle = {
  pending: 'bg-amber-50 text-amber-700 border-amber-200',
  active: 'bg-green-50 text-green-700 border-green-200',
  inactive: 'bg-slate-100 text-slate-500 border-slate-200',
}

async function loadUsers() {
  loading.value = true
  error.value = ''
  try {
    const { data } = await apiClient.get('/admin/users')
    users.value = data
  } catch (err) {
    error.value = err.response?.data?.detail || 'Kullanıcılar yüklenemedi.'
  } finally {
    loading.value = false
  }
}

async function updateStatus(user, status) {
  actionError.value = ''
  try {
    await apiClient.patch(`/admin/users/${user.id}`, { status })
    await loadUsers()
  } catch (err) {
    actionError.value = err.response?.data?.detail || 'İşlem başarısız oldu.'
  }
}

async function submitResetPassword(user) {
  actionError.value = ''
  try {
    await apiClient.patch(`/admin/users/${user.id}`, { new_password: newPassword.value })
    resetPasswordFor.value = null
    newPassword.value = ''
    await loadUsers()
  } catch (err) {
    actionError.value = err.response?.data?.detail || 'Şifre güncellenemedi.'
  }
}

async function submitCreateUser() {
  actionError.value = ''
  creating.value = true
  try {
    await apiClient.post('/admin/users', newUser.value)
    newUser.value = { username_or_email: '', password: '', role: 'user', status: 'active' }
    showCreateForm.value = false
    await loadUsers()
  } catch (err) {
    actionError.value = err.response?.data?.detail || 'Kullanıcı oluşturulamadı.'
  } finally {
    creating.value = false
  }
}

onMounted(loadUsers)
</script>

<template>
  <div class="max-w-5xl mx-auto px-4 py-10">
    <div class="flex items-center justify-between mb-6">
      <div>
        <h1 class="text-2xl font-bold text-slate-800 mb-1">Kullanıcı Yönetimi</h1>
        <p class="text-slate-500">Kayıtları onayla, kullanıcı oluştur, şifre sıfırla.</p>
      </div>
      <button
        @click="showCreateForm = !showCreateForm"
        class="bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-medium px-4 py-2 rounded-lg transition"
      >
        {{ showCreateForm ? 'Vazgeç' : '+ Yeni Kullanıcı' }}
      </button>
    </div>

    <p v-if="error" class="text-sm text-red-600 bg-red-50 border border-red-100 rounded-lg px-3 py-2 mb-4">
      {{ error }}
    </p>
    <p v-if="actionError" class="text-sm text-red-600 bg-red-50 border border-red-100 rounded-lg px-3 py-2 mb-4">
      {{ actionError }}
    </p>

    <div v-if="showCreateForm" class="bg-white rounded-2xl shadow-sm border border-slate-100 p-6 mb-8 space-y-4">
      <div class="grid grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium text-slate-700 mb-1">Kullanıcı adı / E-posta</label>
          <input
            v-model="newUser.username_or_email"
            type="text"
            class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-slate-700 mb-1">Şifre</label>
          <input
            v-model="newUser.password"
            type="text"
            class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-slate-700 mb-1">Rol</label>
          <select
            v-model="newUser.role"
            class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            <option value="user">user</option>
            <option value="admin">admin</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-slate-700 mb-1">Durum</label>
          <select
            v-model="newUser.status"
            class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            <option value="active">active</option>
            <option value="pending">pending</option>
            <option value="inactive">inactive</option>
          </select>
        </div>
      </div>
      <button
        @click="submitCreateUser"
        :disabled="creating"
        class="bg-indigo-600 hover:bg-indigo-700 disabled:opacity-60 text-white text-sm font-medium px-4 py-2 rounded-lg transition"
      >
        {{ creating ? 'Oluşturuluyor...' : 'Kullanıcıyı Oluştur' }}
      </button>
    </div>

    <div v-if="pendingUsers.length" class="mb-8">
      <h2 class="text-sm font-semibold text-amber-600 mb-3">Onay Bekleyenler ({{ pendingUsers.length }})</h2>
      <ul class="space-y-2">
        <li
          v-for="user in pendingUsers"
          :key="user.id"
          class="bg-amber-50 border border-amber-200 rounded-lg px-4 py-3 flex items-center justify-between"
        >
          <span class="text-sm text-slate-800">{{ user.username_or_email }}</span>
          <div class="flex gap-2">
            <button
              @click="updateStatus(user, 'active')"
              class="text-xs font-medium bg-green-600 hover:bg-green-700 text-white px-3 py-1.5 rounded-md transition"
            >
              Onayla
            </button>
            <button
              @click="updateStatus(user, 'inactive')"
              class="text-xs font-medium bg-slate-500 hover:bg-slate-600 text-white px-3 py-1.5 rounded-md transition"
            >
              Reddet
            </button>
          </div>
        </li>
      </ul>
    </div>

    <div class="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-x-auto">
      <table class="w-full text-sm">
        <thead>
          <tr class="text-left text-slate-500 border-b border-slate-100">
            <th class="px-4 py-3 font-medium">Kullanıcı</th>
            <th class="px-4 py-3 font-medium">Rol</th>
            <th class="px-4 py-3 font-medium">Durum</th>
            <th class="px-4 py-3 font-medium">Kayıt Tarihi</th>
            <th class="px-4 py-3 font-medium">İşlemler</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="loading">
            <td colspan="5" class="px-4 py-6 text-center text-slate-400">Yükleniyor...</td>
          </tr>
          <tr v-else-if="!otherUsers.length">
            <td colspan="5" class="px-4 py-6 text-center text-slate-400">Kullanıcı yok.</td>
          </tr>
          <tr v-for="user in otherUsers" :key="user.id" class="border-b border-slate-50 last:border-0">
            <td class="px-4 py-3 text-slate-700">{{ user.username_or_email }}</td>
            <td class="px-4 py-3 text-slate-500">{{ user.role }}</td>
            <td class="px-4 py-3">
              <span :class="['text-xs px-2 py-1 rounded-full border', statusStyle[user.status]]">
                {{ statusLabel[user.status] }}
              </span>
            </td>
            <td class="px-4 py-3 text-slate-500 whitespace-nowrap">
              {{ new Date(user.created_at).toLocaleDateString('tr-TR') }}
            </td>
            <td class="px-4 py-3 space-x-2">
              <template v-if="user.role !== 'admin'">
                <button
                  v-if="user.status === 'active'"
                  @click="updateStatus(user, 'inactive')"
                  class="text-xs font-medium text-slate-600 hover:text-slate-800 underline"
                >
                  Pasife Al
                </button>
                <button
                  v-else
                  @click="updateStatus(user, 'active')"
                  class="text-xs font-medium text-green-600 hover:text-green-800 underline"
                >
                  Aktif Et
                </button>
              </template>
              <span v-else class="text-xs text-slate-400 italic">admin hesabı korunuyor</span>
              <button
                @click="resetPasswordFor = resetPasswordFor === user.id ? null : user.id"
                class="text-xs font-medium text-indigo-600 hover:text-indigo-800 underline"
              >
                Şifre Sıfırla
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div
      v-if="resetPasswordFor"
      class="fixed inset-0 bg-black/30 flex items-center justify-center px-4"
      @click.self="resetPasswordFor = null"
    >
      <div class="bg-white rounded-2xl shadow-xl p-6 w-full max-w-sm">
        <h3 class="font-semibold text-slate-800 mb-4">Yeni Şifre Belirle</h3>
        <input
          v-model="newPassword"
          type="text"
          placeholder="Yeni şifre"
          class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 mb-4"
        />
        <div class="flex gap-2 justify-end">
          <button
            @click="resetPasswordFor = null"
            class="text-sm px-3 py-2 rounded-lg border border-slate-300 text-slate-600"
          >
            Vazgeç
          </button>
          <button
            @click="submitResetPassword(users.find((u) => u.id === resetPasswordFor))"
            class="text-sm px-4 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-700 text-white font-medium"
          >
            Kaydet
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
