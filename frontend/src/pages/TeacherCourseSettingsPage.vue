<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  approveAllJoinRequests,
  approveJoinRequests,
  deleteCourse,
  enrollStudents,
  getCourse,
  getCourseStudents,
  getJoinRequests,
  getStudents,
  regenerateSignupCode,
  unenrollStudents,
  updateCourse,
} from '@/api'
import type { components } from '@/api/schema.ts'

type Course = components['schemas']['CourseOut']
type Student = components['schemas']['StudentOut']
type JoinRequest = components['schemas']['CourseJoinRequestItemOut']

const route = useRoute()
const router = useRouter()
const courseId = route.params.id as string

const course = ref<Course | null>(null)
const name = ref('')
const description = ref('')
const allStudents = ref<Student[]>([])
const enrolledIds = ref<Set<string>>(new Set())
const selectedEnrolled = ref<Set<string>>(new Set())
const selectedAvailable = ref<Set<string>>(new Set())
const filter = ref('')
const loading = ref(true)
const busy = ref(false)
const error = ref('')
const savedFlash = ref(false)
const copyFlash = ref('')
const pendingRequests = ref<JoinRequest[]>([])
const pendingLoading = ref(true)

const filterLower = computed(() => filter.value.trim().toLowerCase())

function matchesFilter(s: Student) {
  if (!filterLower.value) return true
  return s.username.toLowerCase().includes(filterLower.value)
}

const enrolled = computed(() =>
  allStudents.value.filter((s) => enrolledIds.value.has(s.uuid) && matchesFilter(s)),
)
const available = computed(() =>
  allStudents.value.filter((s) => !enrolledIds.value.has(s.uuid) && matchesFilter(s)),
)

const enrolledTotal = computed(
  () => allStudents.value.filter((s) => enrolledIds.value.has(s.uuid)).length,
)

const allEnrolledSelected = computed(
  () =>
    enrolled.value.length > 0 && enrolled.value.every((s) => selectedEnrolled.value.has(s.uuid)),
)
const allAvailableSelected = computed(
  () =>
    available.value.length > 0 && available.value.every((s) => selectedAvailable.value.has(s.uuid)),
)

const inviteLink = computed(() => {
  const code = course.value?.signup_code
  if (!code) return ''
  return `${window.location.origin}/join/${code}`
})

async function loadPending() {
  pendingLoading.value = true
  try {
    pendingRequests.value = await getJoinRequests(courseId)
  } catch {
    pendingRequests.value = []
  } finally {
    pendingLoading.value = false
  }
}

async function load() {
  error.value = ''
  loading.value = true
  try {
    const [courseRes, enrolledRes, studentsRes] = await Promise.all([
      getCourse(courseId),
      getCourseStudents(courseId),
      getStudents(),
    ])
    course.value = courseRes
    name.value = courseRes.name
    description.value = courseRes.description
    enrolledIds.value = new Set(enrolledRes.map((s) => s.uuid))
    allStudents.value = studentsRes ?? []
    selectedEnrolled.value = new Set()
    selectedAvailable.value = new Set()
    await loadPending()
  } catch {
    error.value = 'Could not load course'
  } finally {
    loading.value = false
  }
}

onMounted(load)

async function copyText(label: string, text: string) {
  try {
    await navigator.clipboard.writeText(text)
    copyFlash.value = label
    window.setTimeout(() => {
      if (copyFlash.value === label) copyFlash.value = ''
    }, 1500)
  } catch {
    error.value = `Could not copy ${label.toLowerCase()}`
  }
}

async function onRegenerateCode() {
  if (
    !window.confirm('Generate a new signup code? The old code and invite link will stop working.')
  ) {
    return
  }
  error.value = ''
  busy.value = true
  try {
    course.value = await regenerateSignupCode(courseId)
  } catch {
    error.value = 'Could not regenerate signup code'
  } finally {
    busy.value = false
  }
}

async function enrollPendingOne(studentUuid: string) {
  error.value = ''
  busy.value = true
  try {
    await approveJoinRequests(courseId, [studentUuid])
    enrolledIds.value = new Set([...enrolledIds.value, studentUuid])
    pendingRequests.value = pendingRequests.value.filter((r) => r.uuid !== studentUuid)
  } catch {
    error.value = 'Could not enroll student'
  } finally {
    busy.value = false
  }
}

async function enrollAllPending() {
  if (pendingRequests.value.length === 0) return
  error.value = ''
  busy.value = true
  try {
    await approveAllJoinRequests(courseId)
    const ids = pendingRequests.value.map((r) => r.uuid)
    enrolledIds.value = new Set([...enrolledIds.value, ...ids])
    pendingRequests.value = []
  } catch {
    error.value = 'Could not enroll pending students'
  } finally {
    busy.value = false
  }
}

function toggleSet(set: Set<string>, uuid: string, checked: boolean) {
  const next = new Set(set)
  if (checked) next.add(uuid)
  else next.delete(uuid)
  return next
}

function toggleEnrolledOne(uuid: string, checked: boolean) {
  selectedEnrolled.value = toggleSet(selectedEnrolled.value, uuid, checked)
}

function toggleAvailableOne(uuid: string, checked: boolean) {
  selectedAvailable.value = toggleSet(selectedAvailable.value, uuid, checked)
}

function toggleEnrolledAll(checked: boolean) {
  selectedEnrolled.value = checked ? new Set(enrolled.value.map((s) => s.uuid)) : new Set()
}

function toggleAvailableAll(checked: boolean) {
  selectedAvailable.value = checked ? new Set(available.value.map((s) => s.uuid)) : new Set()
}

async function onSave() {
  error.value = ''
  busy.value = true
  savedFlash.value = false
  try {
    course.value = await updateCourse(courseId, {
      name: name.value,
      description: description.value,
    })
    savedFlash.value = true
  } catch {
    error.value = 'Could not save course'
  } finally {
    busy.value = false
  }
}

async function onDelete() {
  if (
    !window.confirm(
      `Delete “${name.value}” and all of its words, tags, and links? This cannot be undone.`,
    )
  ) {
    return
  }
  error.value = ''
  busy.value = true
  try {
    await deleteCourse(courseId)
    await router.push('/user-start')
  } catch {
    error.value = 'Could not delete course'
    busy.value = false
  }
}

async function enrollSelected() {
  if (selectedAvailable.value.size === 0) return
  error.value = ''
  busy.value = true
  const ids = [...selectedAvailable.value]
  try {
    await enrollStudents(courseId, ids)
    enrolledIds.value = new Set([...enrolledIds.value, ...ids])
    selectedAvailable.value = new Set()
  } catch {
    error.value = 'Could not enroll selected students'
  } finally {
    busy.value = false
  }
}

async function unenrollSelected() {
  if (selectedEnrolled.value.size === 0) return
  error.value = ''
  busy.value = true
  const ids = [...selectedEnrolled.value]
  try {
    await unenrollStudents(courseId, ids)
    const next = new Set(enrolledIds.value)
    for (const id of ids) next.delete(id)
    enrolledIds.value = next
    selectedEnrolled.value = new Set()
  } catch {
    error.value = 'Could not remove selected students'
  } finally {
    busy.value = false
  }
}

async function enrollAllFiltered() {
  if (available.value.length === 0) return
  selectedAvailable.value = new Set(available.value.map((s) => s.uuid))
  await enrollSelected()
}

async function unenrollAllFiltered() {
  if (enrolled.value.length === 0) return
  if (!window.confirm(`Remove ${enrolled.value.length} student(s) from this course?`)) return
  selectedEnrolled.value = new Set(enrolled.value.map((s) => s.uuid))
  await unenrollSelected()
}
</script>

<template>
  <div class="settings">
    <header class="page-header">
      <div>
        <p class="eyebrow">Teacher tools</p>
        <h1>Course settings</h1>
        <p class="ll-muted">Edit details, enroll students, or delete this course.</p>
      </div>
      <router-link class="ll-btn ll-btn-ghost" to="/user-start">← Courses</router-link>
    </header>

    <p v-if="error" class="ll-error">{{ error }}</p>
    <p v-if="loading" class="ll-loading" aria-live="polite">Loading course…</p>

    <template v-else>
      <form class="ll-panel" @submit.prevent="onSave">
        <h2>Details</h2>
        <label class="ll-field">
          Name
          <input v-model="name" required maxlength="100" />
        </label>
        <label class="ll-field">
          Description
          <textarea v-model="description" rows="3" class="ll-input" />
        </label>
        <div class="row-actions">
          <button type="submit" class="ll-btn ll-btn-primary" :disabled="busy">
            {{ busy ? 'Saving…' : 'Save' }}
          </button>
          <span v-if="savedFlash" class="ll-muted saved">Saved</span>
        </div>
      </form>

      <section v-if="course?.signup_code" class="ll-panel signup">
        <h2>Signup code</h2>
        <p class="ll-muted">Share this code or invite link so students can request enrollment.</p>
        <p class="signup-code" aria-label="Signup code">{{ course.signup_code }}</p>
        <div class="row-actions wrap">
          <button
            type="button"
            class="ll-btn"
            :disabled="busy"
            @click="copyText('Code', course.signup_code!)"
          >
            Copy code
          </button>
          <button
            type="button"
            class="ll-btn"
            :disabled="busy"
            @click="copyText('Link', inviteLink)"
          >
            Copy invite link
          </button>
          <button
            type="button"
            class="ll-btn ll-btn-ghost"
            :disabled="busy"
            @click="onRegenerateCode"
          >
            Regenerate code
          </button>
          <span v-if="copyFlash" class="ll-muted saved">{{ copyFlash }} copied</span>
        </div>
      </section>

      <section class="ll-panel pending">
        <div class="roster-header">
          <h2>Pending requests</h2>
          <button
            type="button"
            class="ll-btn ll-btn-primary"
            :disabled="busy || pendingLoading || pendingRequests.length === 0"
            @click="enrollAllPending"
          >
            Enroll all
          </button>
        </div>
        <p v-if="pendingLoading" class="ll-loading" aria-live="polite">Loading requests…</p>
        <ul v-else-if="pendingRequests.length" class="student-list">
          <li v-for="req in pendingRequests" :key="req.uuid">
            <div class="pending-row">
              <span class="username">{{ req.username }}</span>
              <button
                type="button"
                class="ll-btn ll-btn-ghost"
                :disabled="busy"
                @click="enrollPendingOne(req.uuid)"
              >
                Enroll
              </button>
            </div>
          </li>
        </ul>
        <p v-else class="ll-muted empty-hint">No pending enrollment requests.</p>
      </section>

      <section class="ll-panel roster">
        <div class="roster-header">
          <h2>Students</h2>
          <label class="ll-field filter-field">
            Filter
            <input
              v-model="filter"
              type="search"
              placeholder="Search usernames…"
              class="ll-input"
            />
          </label>
        </div>

        <div class="roster-columns">
          <div class="roster-col">
            <div class="col-header">
              <h3>Enrolled ({{ enrolledTotal }})</h3>
              <div class="col-actions">
                <button
                  type="button"
                  class="ll-btn ll-btn-ghost"
                  :disabled="busy || selectedEnrolled.size === 0"
                  @click="unenrollSelected"
                >
                  Remove selected ({{ selectedEnrolled.size }})
                </button>
                <button
                  type="button"
                  class="ll-btn ll-btn-ghost"
                  :disabled="busy || enrolled.length === 0"
                  @click="unenrollAllFiltered"
                >
                  Remove all{{ filter ? ' matching' : '' }}
                </button>
              </div>
            </div>
            <label v-if="enrolled.length" class="select-all">
              <input
                type="checkbox"
                :checked="allEnrolledSelected"
                @change="toggleEnrolledAll(($event.target as HTMLInputElement).checked)"
              />
              Select all shown
            </label>
            <ul v-if="enrolled.length" class="student-list">
              <li v-for="s in enrolled" :key="s.uuid">
                <label class="student-row">
                  <input
                    type="checkbox"
                    :checked="selectedEnrolled.has(s.uuid)"
                    @change="toggleEnrolledOne(s.uuid, ($event.target as HTMLInputElement).checked)"
                  />
                  <span class="username">{{ s.username }}</span>
                </label>
              </li>
            </ul>
            <p v-else class="ll-muted empty-hint">
              {{ filter ? 'No enrolled students match the filter.' : 'No students enrolled yet.' }}
            </p>
          </div>

          <div class="roster-col">
            <div class="col-header">
              <h3>Not enrolled ({{ available.length }}{{ filter ? ' shown' : '' }})</h3>
              <div class="col-actions">
                <button
                  type="button"
                  class="ll-btn ll-btn-primary"
                  :disabled="busy || selectedAvailable.size === 0"
                  @click="enrollSelected"
                >
                  Enroll selected ({{ selectedAvailable.size }})
                </button>
                <button
                  type="button"
                  class="ll-btn"
                  :disabled="busy || available.length === 0"
                  @click="enrollAllFiltered"
                >
                  Enroll all{{ filter ? ' matching' : '' }}
                </button>
              </div>
            </div>
            <label v-if="available.length" class="select-all">
              <input
                type="checkbox"
                :checked="allAvailableSelected"
                @change="toggleAvailableAll(($event.target as HTMLInputElement).checked)"
              />
              Select all shown
            </label>
            <ul v-if="available.length" class="student-list">
              <li v-for="s in available" :key="s.uuid">
                <label class="student-row">
                  <input
                    type="checkbox"
                    :checked="selectedAvailable.has(s.uuid)"
                    @change="
                      toggleAvailableOne(s.uuid, ($event.target as HTMLInputElement).checked)
                    "
                  />
                  <span class="username">{{ s.username }}</span>
                </label>
              </li>
            </ul>
            <p v-else class="ll-muted empty-hint">
              <template v-if="filter">No available students match the filter.</template>
              <template v-else>
                All of your students are enrolled, or you have not created any yet.
                <router-link to="/teacher/students">Manage students</router-link>
              </template>
            </p>
          </div>
        </div>
      </section>

      <section class="ll-panel danger-zone">
        <h2>Delete course</h2>
        <p class="ll-muted">Permanently removes this course and all of its vocabulary content.</p>
        <button type="button" class="ll-btn ll-btn-danger" :disabled="busy" @click="onDelete">
          Delete course
        </button>
      </section>
    </template>
  </div>
</template>

<style scoped>
.settings {
  width: min(100% - 2rem, 56rem);
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

.ll-panel {
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

.row-actions {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.row-actions.wrap {
  flex-wrap: wrap;
}

.signup-code {
  margin: 0;
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  font-size: 2rem;
  font-weight: 700;
  letter-spacing: 0.2em;
}

.pending-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.65rem;
  padding: 0.5rem 0.65rem;
  border-bottom: 1px solid var(--ll-border);
}

.student-list li:last-child .pending-row {
  border-bottom: none;
}

.saved {
  font-size: 0.9rem;
}

.roster-header {
  display: flex;
  flex-wrap: wrap;
  align-items: flex-end;
  justify-content: space-between;
  gap: 0.75rem;
}

.filter-field {
  min-width: min(100%, 14rem);
}

.roster-columns {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.25rem;
}

.roster-col {
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
  min-width: 0;
}

.col-header {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.col-header h3 {
  margin: 0;
  font-family: var(--ll-font-display);
  font-size: 1.05rem;
}

.col-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
}

.select-all {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: var(--ll-ink-muted);
  font-weight: 500;
  cursor: pointer;
}

.student-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  max-height: 22rem;
  overflow-y: auto;
  border: 1px solid var(--ll-border);
  border-radius: var(--ll-radius);
  background: var(--ll-paper);
}

.student-row {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  padding: 0.5rem 0.65rem;
  cursor: pointer;
  border-bottom: 1px solid var(--ll-border);
  margin: 0;
  font-weight: 500;
}

.student-list li:last-child .student-row {
  border-bottom: none;
}

.student-row:hover {
  background: var(--ll-surface);
}

.username {
  font-weight: 600;
}

.empty-hint {
  font-size: 0.9rem;
}

textarea.ll-input {
  resize: vertical;
  min-height: 4.5rem;
}

.danger-zone {
  border-color: color-mix(in srgb, var(--ll-danger) 35%, var(--ll-border));
}

@media (max-width: 720px) {
  .roster-columns {
    grid-template-columns: 1fr;
  }
}
</style>
