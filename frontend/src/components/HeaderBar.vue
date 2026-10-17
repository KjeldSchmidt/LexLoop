<script setup lang="ts">
import { useNavigationHistoryStore } from '@/stores/navigationHistory'
import { useRouter, useRoute } from 'vue-router'
import { storeToRefs } from 'pinia'
import { ref, watch } from 'vue'
import SearchBar from '@/components/SearchBar.vue'
import type { components } from '@/api/schema.ts'
import { useAuthStore } from '@/stores/auth'

type Node = components['schemas']['NodeOut']

const store = useNavigationHistoryStore()
const { history } = storeToRefs(store)
const router = useRouter()
const route = useRoute()
const auth = useAuthStore()

const props = defineProps<{
  course_id: string
}>()

// Create a mutable local ref that syncs with the prop
const mutableCourseId = ref(props.course_id)

// Watch for prop changes and update the local ref
watch(
  () => props.course_id,
  (newValue) => {
    mutableCourseId.value = newValue
  },
)

function goTo(path: string) {
  router.push(path)
}

function goToClasses() {
  // Get course ID from current route if available
  const courseId = route.params.id as string | undefined
  if (courseId) {
    router.push({ name: 'ClassOverview', params: { id: courseId } })
  } else {
    // Fallback: navigate to user-start to choose a course
    router.push('/user-start')
  }
}

function handleSelect(result: { selected_node: Node }) {
  router.push({ name: 'NodePage', params: { id: result.selected_node.uuid } })
}

async function onLogout() {
  await auth.logout()
  await router.push('/login')
}
</script>

<template>
  <header class="header-bar">
    <nav class="breadcrumbs">
      <template v-for="(item, index) in history" :key="item.path">
        <span
          class="breadcrumb-item"
          :class="{ active: index === history.length - 1 }"
          @click="goTo(item.path)"
        >
          {{ item.name }}
        </span>
        <span v-if="index < history.length - 1" class="separator">&gt;</span>
      </template>
    </nav>

    <div class="search-container">
      <SearchBar v-model:course_id="mutableCourseId" @select="handleSelect" />
    </div>

    <div class="header-actions">
      <button class="header-btn" @click="goToClasses">Back to Classes</button>
      <button class="header-btn" @click="onLogout">Log out</button>
    </div>
  </header>
</template>

<style scoped>
.header-bar {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  padding: 0.75rem var(--ll-space-page);
  border-bottom: 1px solid var(--ll-border);
  background: rgb(255 255 255 / 88%);
  backdrop-filter: blur(10px);
  gap: 1rem;
  position: sticky;
  top: 0;
  z-index: 15;
}

.search-container {
  display: flex;
  justify-content: center;
  width: 100%;
}

.breadcrumbs {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  flex-wrap: wrap;
}

.breadcrumb-item {
  cursor: pointer;
  color: var(--ll-ink-muted);
  font-weight: 500;
}

.breadcrumb-item:hover {
  color: var(--ll-accent);
}

.breadcrumb-item.active {
  color: var(--ll-ink);
  font-weight: 600;
}

.separator {
  color: var(--ll-border);
}

.header-actions {
  display: flex;
  gap: 0.5rem;
  justify-content: flex-end;
  flex-wrap: wrap;
}

.header-btn {
  padding: 0.45rem 0.9rem;
  border: 1.5px solid var(--ll-border);
  border-radius: var(--ll-radius);
  background: var(--ll-surface);
  cursor: pointer;
  font-size: 0.85rem;
  font-weight: 600;
  transition:
    background-color 0.15s ease,
    border-color 0.15s ease;
}

.header-btn:hover {
  background: var(--ll-paper);
  border-color: var(--ll-ink);
}
</style>
