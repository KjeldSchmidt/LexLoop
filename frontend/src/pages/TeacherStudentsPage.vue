<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { bulkCreateStudents, getStudents } from '@/api'
import type { components } from '@/api/schema.ts'

type Student = components['schemas']['StudentOut']
type CreatedCreds = components['schemas']['StudentCreatedCreds']

const students = ref<Student[]>([])
const count = ref(10)
const error = ref('')
const creating = ref(false)
const created = ref<CreatedCreds[]>([])

const credentialsText = computed(() =>
  created.value.map((a) => `${a.username}\t${a.password}`).join('\n'),
)

async function refresh() {
  const res = await getStudents()
  if (res) students.value = res
}

onMounted(refresh)

async function onBulkCreate() {
  error.value = ''
  creating.value = true
  created.value = []
  try {
    const res = await bulkCreateStudents(count.value)
    created.value = res?.accounts ?? []
    await refresh()
  } catch {
    error.value = 'Could not create students'
  } finally {
    creating.value = false
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
        Usernames look like <code>coral-lantern-kite</code>; passwords are phrases like
        <code>brave cedar quietly dances</code>.
      </p>
      <label>
        Number of accounts
        <input v-model.number="count" type="number" min="1" max="100" required />
      </label>
      <button type="submit" :disabled="creating">
        {{ creating ? 'Creating…' : 'Create accounts' }}
      </button>
      <p v-if="error" class="error">{{ error }}</p>
    </form>

    <section v-if="created.length" class="created">
      <h2>New credentials ({{ created.length }})</h2>
      <p class="hint">Download now — passwords are not shown again later.</p>
      <button type="button" @click="downloadCredentials">Download .txt</button>
      <pre class="creds">{{ credentialsText }}</pre>
    </section>

    <section>
      <h2>All students ({{ students.length }})</h2>
      <ul>
        <li v-for="s in students" :key="s.uuid">
          {{ s.username }}
          <span v-if="!s.is_active">(inactive)</span>
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
.created {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
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
.creds {
  margin: 0;
  padding: 0.75rem;
  background: #f6f6f6;
  border: 1px solid #ddd;
  border-radius: 4px;
  overflow-x: auto;
  font-size: 0.85rem;
}
.error {
  color: #a00;
}
</style>
