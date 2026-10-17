<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const { isAuthenticated, isTeacher, student } = storeToRefs(auth)
const router = useRouter()

async function onLogout() {
  await auth.logout()
  await router.push('/login')
}
</script>

<template>
  <div class="app-shell">
    <div v-if="isAuthenticated" class="session-bar">
      <span class="session-label">
        {{ isTeacher ? 'Teacher' : `Student (${student?.username ?? ''})` }}
      </span>
      <button type="button" class="logout-btn" @click="onLogout">Log out</button>
    </div>
    <router-view />
  </div>
</template>

<style scoped>
.app-shell {
  min-height: 100vh;
}
.session-bar {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem 1.5rem;
  border-bottom: 1px solid #ddd;
  background: #fafafa;
  font-size: 0.85rem;
}
.session-label {
  color: #555;
}
.logout-btn {
  padding: 0.35rem 0.75rem;
  border: 1px solid #333;
  border-radius: 4px;
  background: #fff;
  cursor: pointer;
}
.logout-btn:hover {
  background: #f0f0f0;
}
</style>
