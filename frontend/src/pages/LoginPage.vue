<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { studentLogin } from '@/api'

const router = useRouter()
const username = ref('')
const password = ref('')
const error = ref('')
const apiBase = import.meta.env.VITE_API_URL as string

function googleLogin() {
  // fastapi-users Google authorize; cookie set on callback then user returns.
  const authorizeUrl = new URL('auth/google/authorize', apiBase)
  window.location.href = authorizeUrl.toString()
}

async function onStudentLogin() {
  error.value = ''
  try {
    await studentLogin(username.value, password.value)
    await router.push('/user-start')
  } catch {
    error.value = 'Login failed'
  }
}
</script>

<template>
  <div class="login">
    <h1>Sign in</h1>

    <section>
      <h2>Teacher</h2>
      <button type="button" @click="googleLogin">Sign in with Google</button>
    </section>

    <section>
      <h2>Student</h2>
      <form @submit.prevent="onStudentLogin">
        <label>
          Username
          <input v-model="username" autocomplete="username" required />
        </label>
        <label>
          Password
          <input v-model="password" type="password" autocomplete="current-password" required />
        </label>
        <button type="submit">Sign in</button>
      </form>
      <p v-if="error" class="error">{{ error }}</p>
    </section>
  </div>
</template>

<style scoped>
.login {
  max-width: 24rem;
  margin: 2rem auto;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}
section {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
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
