<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { createStudent, getStudents } from '@/api'
import type { components } from '@/api/schema.ts'

type Student = components['schemas']['StudentOut']

const students = ref<Student[]>([])
const username = ref('')
const password = ref('')
const error = ref('')

async function refresh() {
  const res = await getStudents()
  if (res) students.value = res
}

onMounted(refresh)

async function onCreate() {
  error.value = ''
  try {
    await createStudent(username.value, password.value)
    username.value = ''
    password.value = ''
    await refresh()
  } catch {
    error.value = 'Could not create student'
  }
}
</script>

<template>
  <div class="students">
    <h1>Students</h1>
    <p>
      <router-link to="/user-start">Back to courses</router-link>
    </p>

    <form @submit.prevent="onCreate">
      <h2>Create student</h2>
      <label>
        Username
        <input v-model="username" required minlength="3" />
      </label>
      <label>
        Password
        <input v-model="password" type="password" required minlength="8" />
      </label>
      <button type="submit">Create</button>
      <p v-if="error" class="error">{{ error }}</p>
    </form>

    <ul>
      <li v-for="s in students" :key="s.uuid">
        {{ s.username }}
        <span v-if="!s.is_active">(inactive)</span>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.students {
  max-width: 32rem;
  margin: 2rem auto;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
label {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}
.error {
  color: #a00;
}
</style>
