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
    <header class="intro">
      <p class="eyebrow">LexLoop</p>
      <h1>Sign in</h1>
      <p v-if="needsAuthMessage" class="ll-muted notice">
        You need to be logged in to see this page.
      </p>
    </header>

    <section class="ll-panel">
      <h2>Teacher</h2>
      <p class="ll-muted blurb">Continue with your Google account.</p>
      <button
        type="button"
        class="ll-btn ll-btn-primary"
        :disabled="googleLoading"
        @click="onGoogleLogin"
      >
        {{ googleLoading ? 'Waiting for Google…' : 'Sign in with Google' }}
      </button>
    </section>

    <section class="ll-panel">
      <h2>Student</h2>
      <p class="ll-muted blurb">Use the username and passphrase from your teacher.</p>
      <form class="student-form" @submit.prevent="onStudentLogin">
        <label class="ll-field">
          Username
          <input v-model="username" autocomplete="username" required />
        </label>
        <label class="ll-field">
          Password
          <input v-model="password" type="password" autocomplete="current-password" required />
        </label>
        <button type="submit" class="ll-btn ll-btn-primary">Sign in</button>
      </form>
    </section>

    <p v-if="error" class="ll-error">{{ error }}</p>
  </div>
</template>

<style scoped>
.login {
  width: min(100% - 2rem, 26rem);
  margin: 0 auto;
  padding: clamp(2rem, 6vh, 3.5rem) 0 3rem;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  animation: rise 0.45s ease-out both;
}

.intro {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.eyebrow {
  margin: 0;
  font-family: var(--ll-font-display);
  font-weight: 700;
  font-size: 1.1rem;
  color: var(--ll-accent);
}

.notice {
  margin-top: 0.35rem;
}

.ll-panel {
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

.blurb {
  font-size: 0.9rem;
}

.student-form {
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

@keyframes rise {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: none;
  }
}
</style>
