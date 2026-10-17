<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'

const OAUTH_SUCCESS = 'lexloop-oauth-success'

const router = useRouter()

onMounted(async () => {
  if (window.opener && !window.opener.closed) {
    window.opener.postMessage({ type: OAUTH_SUCCESS }, window.location.origin)
    window.close()
    return
  }
  // Full-page fallback (popup blocked or direct navigation)
  await router.replace('/user-start')
})
</script>

<template>
  <p class="hint">Signing you in…</p>
</template>

<style scoped>
.hint {
  margin: 2rem;
  text-align: center;
}
</style>
