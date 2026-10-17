import { onBeforeUnmount, ref } from 'vue'
import { getGoogleAuthorizeUrl } from '@/api'

const OAUTH_SUCCESS = 'lexloop-oauth-success'
const POPUP_WIDTH = 500
const POPUP_HEIGHT = 650

/**
 * Opens Google OAuth in a popup; resolves when the popup reports success.
 */
export function useGoogleLogin() {
  const loading = ref(false)
  const error = ref('')

  let popup: Window | null = null
  let popupPoll: ReturnType<typeof setInterval> | null = null
  let oauthCompleted = false
  let resolveLogin: (() => void) | null = null
  let rejectLogin: ((reason?: Error) => void) | null = null

  function clearPopupWatch() {
    window.removeEventListener('message', onOAuthMessage)
    if (popupPoll !== null) {
      clearInterval(popupPoll)
      popupPoll = null
    }
    popup = null
  }

  function finish(success: boolean, message?: string) {
    clearPopupWatch()
    loading.value = false
    if (success) {
      error.value = ''
      resolveLogin?.()
    } else {
      if (message) error.value = message
      rejectLogin?.(new Error(message ?? 'GOOGLE_LOGIN_FAILED'))
    }
    resolveLogin = null
    rejectLogin = null
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
    finish(true)
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

  async function loginWithGoogle(): Promise<void> {
    error.value = ''
    clearPopupWatch()
    oauthCompleted = false
    loading.value = true

    return new Promise((resolve, reject) => {
      resolveLogin = resolve
      rejectLogin = reject

      void (async () => {
        try {
          const authorizeUrl = await getGoogleAuthorizeUrl()
          popup = openCenteredPopup(authorizeUrl)
          if (!popup) {
            finish(false, 'Popup blocked — allow popups for this site and try again')
            return
          }

          window.addEventListener('message', onOAuthMessage)
          popupPoll = setInterval(() => {
            if (popup && popup.closed) {
              if (!oauthCompleted) {
                finish(false, 'Google sign-in was cancelled')
              }
            }
          }, 500)
        } catch {
          finish(false, 'Could not start Google sign-in')
        }
      })()
    })
  }

  onBeforeUnmount(() => {
    clearPopupWatch()
    loading.value = false
    resolveLogin = null
    rejectLogin = null
  })

  return { loading, error, loginWithGoogle }
}
