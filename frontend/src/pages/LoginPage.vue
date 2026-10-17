<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { studentLogin } from '@/api'
import { useGoogleLogin } from '@/composables/useGoogleLogin'
import { safeRedirectPath } from '@/router/authRedirect'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()

const username = ref('')
const password = ref('')
const formError = ref('')
const { loading: googleLoading, error: googleError, loginWithGoogle } = useGoogleLogin()

const needsAuthMessage = computed(() => route.query.reason === 'auth')
const error = computed(() => formError.value || googleError.value)

async function afterLogin() {
  await auth.refreshSession()
  await router.push(safeRedirectPath(route.query.redirect))
}

async function onGoogleLogin() {
  formError.value = ''
  try {
    await loginWithGoogle()
    await afterLogin()
  } catch {
    // error text comes from useGoogleLogin
  }
}

async function onStudentLogin() {
  formError.value = ''
  try {
    await studentLogin(username.value, password.value)
    await afterLogin()
  } catch {
    formError.value = 'Login failed'
  }
}
</script>

<template>
  <div class="login">
    <h1>Sign in</h1>
    <p v-if="needsAuthMessage" class="notice">You need to be logged in to see this page.</p>

    <section>
      <h2>Teacher</h2>
      <button type="button" :disabled="googleLoading" @click="onGoogleLogin">
        {{ googleLoading ? 'Waiting for Google…' : 'Sign in with Google' }}
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
.notice {
  margin: 0;
  color: #444;
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
