import { defineStore } from 'pinia'
import { ref } from 'vue'

export interface BreadcrumbItem {
  name: string
  path: string
  type: 'class' | 'tag' | 'node'
}

const MAX_HISTORY = 4

export const useNavigationHistoryStore = defineStore('navigationHistory', () => {
  const history = ref<BreadcrumbItem[]>([])

  function pushPage(item: BreadcrumbItem) {
    // Don't add duplicate if it's the same as the last item
    const last = history.value[history.value.length - 1]
    if (last && last.path === item.path) {
      return
    }

    // Check if this page already exists in history
    const existingIndex = history.value.findIndex((h) => h.path === item.path)
    if (existingIndex !== -1) {
      // Truncate history to this point (user navigated back)
      history.value = history.value.slice(0, existingIndex + 1)
    } else {
      // Add new item
      history.value.push(item)
      // Keep only last MAX_HISTORY items
      if (history.value.length > MAX_HISTORY) {
        history.value = history.value.slice(-MAX_HISTORY)
      }
    }
  }

  function resetToClass(className: string) {
    history.value = [{ name: className, path: '/class', type: 'class' }]
  }

  return {
    history,
    pushPage,
    resetToClass,
  }
})
