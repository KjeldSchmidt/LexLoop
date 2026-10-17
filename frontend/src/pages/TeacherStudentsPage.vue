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
  const res = await getStudents()
  if (res) {
    students.value = res
    const valid = new Set(res.map((s) => s.uuid))
    selected.value = new Set([...selected.value].filter((id) => valid.has(id)))
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
    <h1>Students</h1>
    <p>
      <router-link to="/user-start">Back to courses</router-link>
    </p>

    <form class="bulk" @submit.prevent="onBulkCreate">
      <h2>Create accounts</h2>
      <p class="hint">
        Usernames look like <code>CoralLantern</code>; passwords are random four-word passphrases
        (different shape, large word list).
      </p>
      <label>
        Number of accounts
        <input v-model.number="count" type="number" min="1" max="100" required />
      </label>
      <button type="submit" :disabled="busy">
        {{ busy ? 'Working…' : 'Create accounts' }}
      </button>
    </form>

    <section v-if="created.length" class="created">
      <h2>{{ credentialsTitle }} ({{ created.length }})</h2>
      <p class="hint">Download now — passwords are not shown again later.</p>
      <button type="button" @click="downloadCredentials">Download .txt</button>
      <pre class="creds">{{ credentialsText }}</pre>
    </section>

    <section class="list">
      <div class="list-header">
        <h2>All students ({{ students.length }})</h2>
        <div class="actions" v-if="students.length">
          <button type="button" :disabled="busy || selectedCount === 0" @click="onBulkNewPasswords">
            New passwords ({{ selectedCount }})
          </button>
          <button
            type="button"
            class="danger"
            :disabled="busy || selectedCount === 0"
            @click="onBulkDelete"
          >
            Delete ({{ selectedCount }})
          </button>
        </div>
      </div>
      <p v-if="error" class="error">{{ error }}</p>
      <label v-if="students.length" class="select-all">
        <input
          type="checkbox"
          :checked="allSelected"
          @change="toggleAll(($event.target as HTMLInputElement).checked)"
        />
        Select all
      </label>
      <ul>
        <li v-for="s in students" :key="s.uuid">
          <label class="row">
            <input
              type="checkbox"
              :checked="selected.has(s.uuid)"
              @change="toggleOne(s.uuid, ($event.target as HTMLInputElement).checked)"
            />
            <span>{{ s.username }}</span>
            <span v-if="!s.is_active" class="inactive">(inactive)</span>
          </label>
        </li>
      </ul>
    </section>
  </div>
</template>

<style scoped>
.students {
  max-width: 40rem;
  margin: 2rem auto;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}
.bulk,
.created,
.list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}
.list-header {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
}
.list-header h2 {
  margin: 0;
}
.actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}
.hint {
  margin: 0;
  color: #555;
  font-size: 0.9rem;
}
label {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  max-width: 12rem;
}
.select-all,
.row {
  flex-direction: row;
  align-items: center;
  gap: 0.5rem;
  max-width: none;
}
.creds {
  margin: 0;
  padding: 0.75rem;
  background: #f6f6f6;
  border: 1px solid #ddd;
  border-radius: 4px;
  overflow-x: auto;
  font-size: 0.85rem;
}
ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}
.inactive {
  color: #888;
}
.danger {
  color: #a00;
  border-color: #a00;
}
.error {
  color: #a00;
}
</style>
