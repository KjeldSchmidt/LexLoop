<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import {
  bulkCreateStudents,
  bulkDeleteStudents,
  bulkResetStudentPasswords,
  getStudents,
} from '@/api'
import type { components } from '@/api/schema.ts'

type Student = components['schemas']['StudentOut']
type CreatedCreds = components['schemas']['StudentCreatedCreds']

const students = ref<Student[]>([])
const selected = ref<Set<string>>(new Set())
const count = ref(10)
const error = ref('')
const busy = ref(false)
const loading = ref(true)
const created = ref<CreatedCreds[]>([])
const credentialsTitle = ref('New credentials')

const credentialsText = computed(() =>
  created.value.map((a) => `${a.username}\t${a.password}`).join('\n'),
)

const allSelected = computed(
  () => students.value.length > 0 && selected.value.size === students.value.length,
)

const selectedCount = computed(() => selected.value.size)

async function refresh() {
  loading.value = true
  try {
    const res = await getStudents()
    if (res) {
      students.value = res
      const valid = new Set(res.map((s) => s.uuid))
      selected.value = new Set([...selected.value].filter((id) => valid.has(id)))
    }
  } finally {
    loading.value = false
  }
}

onMounted(refresh)

function toggleOne(uuid: string, checked: boolean) {
  const next = new Set(selected.value)
  if (checked) next.add(uuid)
  else next.delete(uuid)
  selected.value = next
}

function toggleAll(checked: boolean) {
  selected.value = checked ? new Set(students.value.map((s) => s.uuid)) : new Set()
}

async function onBulkCreate() {
  error.value = ''
  busy.value = true
  created.value = []
  try {
    const res = await bulkCreateStudents(count.value)
    created.value = res?.accounts ?? []
    credentialsTitle.value = 'New credentials'
    selected.value = new Set()
    await refresh()
  } catch {
    error.value = 'Could not create students'
  } finally {
    busy.value = false
  }
}

async function onBulkDelete() {
  if (selected.value.size === 0) return
  if (
    !window.confirm(
      `Permanently delete ${selected.value.size} student account(s)? This cannot be undone.`,
    )
  ) {
    return
  }
  error.value = ''
  busy.value = true
  try {
    await bulkDeleteStudents([...selected.value])
    created.value = []
    selected.value = new Set()
    await refresh()
  } catch {
    error.value = 'Could not delete selected students'
  } finally {
    busy.value = false
  }
}

async function onBulkNewPasswords() {
  if (selected.value.size === 0) return
  error.value = ''
  busy.value = true
  created.value = []
  try {
    const res = await bulkResetStudentPasswords([...selected.value])
    created.value = res?.accounts ?? []
    credentialsTitle.value = 'Reset passwords'
    selected.value = new Set()
    await refresh()
  } catch {
    error.value = 'Could not reset passwords'
  } finally {
    busy.value = false
  }
}

function downloadCredentials() {
  const body = [
    '# LexLoop student accounts',
    '# username<TAB>password',
    credentialsText.value,
    '',
  ].join('\n')
  const blob = new Blob([body], { type: 'text/plain;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const anchor = document.createElement('a')
  anchor.href = url
  anchor.download = `lexloop-students-${created.value.length}.txt`
  anchor.click()
  URL.revokeObjectURL(url)
}
</script>

<template>
  <div class="students">
    <header class="page-header">
      <div>
        <p class="eyebrow">Teacher tools</p>
        <h1>Students</h1>
        <p class="ll-muted">Create accounts and share credentials with your class.</p>
      </div>
      <router-link class="ll-btn ll-btn-ghost" to="/user-start">← Courses</router-link>
    </header>

    <form class="ll-panel bulk" @submit.prevent="onBulkCreate">
      <h2>Create accounts</h2>
      <p class="ll-muted hint">
        Usernames look like <code>CoralLantern</code>; passwords look like
        <code>calm-ticket-quietly-dances</code>.
      </p>
      <div class="bulk-row">
        <label class="ll-field count-field">
          Number of accounts
          <input v-model.number="count" type="number" min="1" max="100" required />
        </label>
        <button type="submit" class="ll-btn ll-btn-primary" :disabled="busy">
          {{ busy ? 'Working…' : 'Create accounts' }}
        </button>
      </div>
    </form>

    <section v-if="created.length" class="ll-panel created">
      <div class="created-header">
        <div>
          <h2>{{ credentialsTitle }} ({{ created.length }})</h2>
          <p class="ll-muted hint">Download now — passwords are not shown again later.</p>
        </div>
        <button type="button" class="ll-btn ll-btn-primary" @click="downloadCredentials">
          Download .txt
        </button>
      </div>
      <pre class="creds">{{ credentialsText }}</pre>
    </section>

    <section class="ll-panel list">
      <div class="list-header">
        <h2>{{ loading ? 'All students' : `All students (${students.length})` }}</h2>
        <div v-if="!loading && students.length" class="actions">
          <button
            type="button"
            class="ll-btn"
            :disabled="busy || selectedCount === 0"
            @click="onBulkNewPasswords"
          >
            New passwords ({{ selectedCount }})
          </button>
          <button
            type="button"
            class="ll-btn ll-btn-danger"
            :disabled="busy || selectedCount === 0"
            @click="onBulkDelete"
          >
            Delete ({{ selectedCount }})
          </button>
        </div>
      </div>
      <p v-if="error" class="ll-error">{{ error }}</p>
      <p v-if="loading" class="ll-loading" aria-live="polite">Loading students…</p>
      <template v-else>
        <label v-if="students.length" class="select-all">
          <input
            type="checkbox"
            :checked="allSelected"
            @change="toggleAll(($event.target as HTMLInputElement).checked)"
          />
          Select all
        </label>
        <ul v-if="students.length">
          <li v-for="s in students" :key="s.uuid">
            <label class="row">
              <input
                type="checkbox"
                :checked="selected.has(s.uuid)"
                @change="toggleOne(s.uuid, ($event.target as HTMLInputElement).checked)"
              />
              <span class="username">{{ s.username }}</span>
              <span v-if="!s.is_active" class="badge">Inactive</span>
            </label>
          </li>
        </ul>
        <p v-else class="ll-muted empty">No students yet — create a batch above.</p>
      </template>
    </section>
  </div>
</template>

<style scoped>
.students {
  width: min(100% - 2rem, 42rem);
  margin: 0 auto;
  padding: var(--ll-space-page) 0 3rem;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.page-header {
  display: flex;
  flex-wrap: wrap;
  align-items: flex-end;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 0.25rem;
}

.page-header > div {
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

.bulk,
.created,
.list {
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

.hint {
  font-size: 0.9rem;
}

.bulk-row {
  display: flex;
  flex-wrap: wrap;
  align-items: flex-end;
  gap: 0.75rem;
}

.count-field {
  max-width: 10rem;
}

.created-header,
.list-header {
  display: flex;
  flex-wrap: wrap;
  align-items: flex-start;
  justify-content: space-between;
  gap: 0.75rem;
}

.created-header > div,
.list-header h2 {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.creds {
  margin: 0;
  padding: 0.9rem 1rem;
  background: var(--ll-paper);
  border: 1px solid var(--ll-border);
  border-radius: var(--ll-radius);
  overflow-x: auto;
  font-size: 0.85rem;
  line-height: 1.55;
}

.select-all,
.row {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 0.65rem;
  max-width: none;
  font-weight: 500;
  cursor: pointer;
}

.select-all {
  color: var(--ll-ink-muted);
  font-size: 0.9rem;
}

ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.row {
  padding: 0.55rem 0.7rem;
  border-radius: var(--ll-radius);
  border: 1px solid transparent;
  transition:
    background-color 0.12s ease,
    border-color 0.12s ease;
}

.row:hover {
  background: var(--ll-paper);
  border-color: var(--ll-border);
}

.username {
  font-weight: 600;
}

.badge {
  margin-left: auto;
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--ll-ink-muted);
  background: var(--ll-paper-deep);
  padding: 0.15rem 0.5rem;
  border-radius: var(--ll-radius-pill);
}

.empty {
  text-align: center;
  padding: 0.5rem 0;
}
</style>
