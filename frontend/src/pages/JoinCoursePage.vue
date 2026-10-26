<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { getCourseByCode, requestCourseJoin } from '@/api'

const route = useRoute()
const code = (route.params.code as string).toUpperCase()

const courseName = ref('')
const loading = ref(true)
const busy = ref(false)
const error = ref('')
const status = ref('')

async function load() {
  error.value = ''
  loading.value = true
  try {
    const preview = await getCourseByCode(code)
    courseName.value = preview.course_name
  } catch {
    error.value = 'This invite code is invalid or no longer works.'
  } finally {
    loading.value = false
  }
}

onMounted(load)

async function onRequest() {
  error.value = ''
  busy.value = true
  try {
    const result = await requestCourseJoin(code)
    if (result.status === 'pending' || result.status === 'already_pending') {
      status.value = `Request sent for “${result.course_name}”. Your teacher will approve it.`
    } else if (result.status === 'already_enrolled') {
      status.value = `You are already enrolled in “${result.course_name}”.`
    } else {
      status.value = `Done for “${result.course_name}”.`
    }
  } catch {
    error.value = 'Could not send enrollment request.'
  } finally {
    busy.value = false
  }
}
</script>

<template>
  <div class="join">
    <header class="page-header">
      <p class="eyebrow">Course invite</p>
      <h1>Join a course</h1>
    </header>

    <p v-if="loading" class="ll-loading" aria-live="polite">Looking up invite…</p>
    <p v-else-if="error" class="ll-error">{{ error }}</p>

    <template v-else>
      <section class="ll-panel">
        <p class="ll-muted">Signup code</p>
        <p class="code">{{ code }}</p>
        <p class="course-name">{{ courseName }}</p>
        <p v-if="status" class="success">{{ status }}</p>
        <button
          v-else
          type="button"
          class="ll-btn ll-btn-primary"
          :disabled="busy"
          @click="onRequest"
        >
          {{ busy ? 'Sending…' : 'Request enrollment' }}
        </button>
      </section>
      <router-link class="ll-btn ll-btn-ghost" to="/user-start">← Your courses</router-link>
    </template>
  </div>
</template>

<style scoped>
.join {
  width: min(100% - 2rem, 28rem);
  margin: 0 auto;
  padding: var(--ll-space-page) 0 3rem;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.page-header {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.eyebrow {
  margin: 0;
  font-size: 0.8rem;
  font-weight: 600;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--ll-accent);
}

.ll-panel {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.code {
  margin: 0;
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  font-size: 2rem;
  font-weight: 700;
  letter-spacing: 0.2em;
}

.course-name {
  margin: 0;
  font-size: 1.15rem;
  font-weight: 600;
}

.success {
  margin: 0;
  color: var(--ll-ink);
  font-weight: 500;
}
</style>
