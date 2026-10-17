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
    <header v-if="isAuthenticated" class="session-bar">
      <router-link class="brand" to="/user-start" title="All courses">LexLoop</router-link>
      <div class="session-actions">
        <span class="session-label">
          {{ isTeacher ? 'Teacher' : `Student · ${student?.username ?? ''}` }}
        </span>
        <button type="button" class="ll-btn ll-btn-ghost logout-btn" @click="onLogout">
          Log out
        </button>
      </div>
    </header>
    <router-view />
  </div>
</template>

<style scoped>
.app-shell {
  min-height: 100vh;
}

.session-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 0.75rem;
  padding: 0.65rem var(--ll-space-page);
  border-bottom: 1px solid var(--ll-border);
  background: rgb(255 255 255 / 90%);
  backdrop-filter: blur(10px);
  position: sticky;
  top: 0;
  z-index: 30;
}

.brand {
  font-family: var(--ll-font-display);
  font-weight: 700;
  font-size: 1.05rem;
  letter-spacing: -0.02em;
  color: var(--ll-ink);
  text-decoration: none;
}

.brand:hover {
  color: var(--ll-accent);
}

.session-actions {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.session-label {
  color: var(--ll-ink-muted);
  font-size: 0.875rem;
  font-weight: 500;
}

.logout-btn {
  padding: 0.35rem 0.8rem;
  font-size: 0.85rem;
}
</style>
