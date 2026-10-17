<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { getGoogleAuthorizeUrl, studentLogin } from '@/api'

const router = useRouter()
const username = ref('')
const password = ref('')
const error = ref('')
const googleLoading = ref(false)

async function googleLogin() {
  // fastapi-users returns JSON { authorization_url }; redirect the browser there.
  error.value = ''
  googleLoading.value = true
  try {
    window.location.href = await getGoogleAuthorizeUrl()
  } catch {
    error.value = 'Could not start Google sign-in'
    googleLoading.value = false
  }
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
      <button type="button" :disabled="googleLoading" @click="googleLogin">
        {{ googleLoading ? 'Redirecting…' : 'Sign in with Google' }}
      </button>
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
    </section>

    <p v-if="error" class="error">{{ error }}</p>
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
