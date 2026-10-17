<script setup lang="ts">
import { onBeforeUnmount, ref } from 'vue'
import { useRouter } from 'vue-router'
import { getGoogleAuthorizeUrl, studentLogin } from '@/api'

const OAUTH_SUCCESS = 'lexloop-oauth-success'
const POPUP_WIDTH = 500
const POPUP_HEIGHT = 650

const router = useRouter()
const username = ref('')
const password = ref('')
const error = ref('')
const googleLoading = ref(false)

let popup: Window | null = null
let popupPoll: ReturnType<typeof setInterval> | null = null
let oauthCompleted = false

function clearPopupWatch() {
  window.removeEventListener('message', onOAuthMessage)
  if (popupPoll !== null) {
    clearInterval(popupPoll)
    popupPoll = null
  }
  popup = null
}

function finishGoogleLogin() {
  clearPopupWatch()
  googleLoading.value = false
}

function onOAuthMessage(event: MessageEvent) {
  if (event.origin !== window.location.origin) return
  if (
    typeof event.data !== 'object' ||
    event.data === null ||
    (event.data as { type?: string }).type !== OAUTH_SUCCESS
  ) {
    return
  }
  oauthCompleted = true
  finishGoogleLogin()
  void router.push('/user-start')
}

function openCenteredPopup(url: string): Window | null {
  const left = Math.round(window.screenX + (window.outerWidth - POPUP_WIDTH) / 2)
  const top = Math.round(window.screenY + (window.outerHeight - POPUP_HEIGHT) / 2)
  return window.open(
    url,
    'lexloop-google-oauth',
    `width=${POPUP_WIDTH},height=${POPUP_HEIGHT},left=${left},top=${top},popup=yes`,
  )
}

async function googleLogin() {
  error.value = ''
  clearPopupWatch()
  oauthCompleted = false
  googleLoading.value = true

  try {
    const authorizeUrl = await getGoogleAuthorizeUrl()
    popup = openCenteredPopup(authorizeUrl)
    if (!popup) {
      error.value = 'Popup blocked — allow popups for this site and try again'
      googleLoading.value = false
      return
    }

    window.addEventListener('message', onOAuthMessage)
    popupPoll = setInterval(() => {
      if (popup && popup.closed) {
        if (!oauthCompleted) {
          error.value = 'Google sign-in was cancelled'
        }
        finishGoogleLogin()
      }
    }, 500)
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

onBeforeUnmount(() => {
  finishGoogleLogin()
})
</script>

<template>
  <div class="login">
    <h1>Sign in</h1>

    <section>
      <h2>Teacher</h2>
      <button type="button" :disabled="googleLoading" @click="googleLogin">
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
