<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import SearchBar from '@/components/SearchBar.vue'
import type { components } from '@/api/schema.ts'
import { useNavigationHistoryStore } from '@/stores/navigationHistory'

type Node = components['schemas']['NodeOut']

const props = defineProps<{
  course_id: string
}>()

const store = useNavigationHistoryStore()
const { history } = storeToRefs(store)
const router = useRouter()
const route = useRoute()

const mutableCourseId = ref(props.course_id)

watch(
  () => props.course_id,
  (newValue) => {
    mutableCourseId.value = newValue
  },
)

const onClassOverview = computed(() => route.name === 'ClassOverview')

function goTo(path: string) {
  router.push(path)
}

function goToClassOverview() {
  router.push({ name: 'ClassOverview', params: { id: props.course_id } })
}

function goToAllCourses() {
  router.push('/user-start')
}

function handleSelect(result: { selected_node: Node }) {
  router.push({ name: 'NodePage', params: { id: result.selected_node.uuid } })
}
</script>

<template>
  <div class="course-bar">
    <nav class="breadcrumbs" aria-label="Course navigation">
      <template v-for="(item, index) in history" :key="item.path">
        <button
          type="button"
          class="breadcrumb-item"
          :class="{ active: index === history.length - 1 }"
          :disabled="index === history.length - 1"
          @click="goTo(item.path)"
        >
          {{ item.name }}
        </button>
        <span v-if="index < history.length - 1" class="separator" aria-hidden="true">/</span>
      </template>
    </nav>

    <div class="search-container">
      <SearchBar v-model:course_id="mutableCourseId" @select="handleSelect" />
    </div>

    <div class="course-actions">
      <button
        v-if="!onClassOverview"
        type="button"
        class="ll-btn ll-btn-ghost course-btn"
        @click="goToClassOverview"
      >
        Class overview
      </button>
      <button v-else type="button" class="ll-btn ll-btn-ghost course-btn" @click="goToAllCourses">
        All courses
      </button>
    </div>
  </div>
</template>

<style scoped>
.course-bar {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(12rem, 22rem) minmax(0, 1fr);
  align-items: center;
  gap: 0.75rem 1rem;
  padding: 0.55rem var(--ll-space-page);
  border-bottom: 1px solid var(--ll-border);
  background: rgb(238 242 246 / 72%);
}

.search-container {
  display: flex;
  justify-content: center;
  width: 100%;
}

.breadcrumbs {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.875rem;
  flex-wrap: wrap;
  min-width: 0;
}

.breadcrumb-item {
  border: none;
  background: none;
  padding: 0.15rem 0.25rem;
  margin: 0;
  cursor: pointer;
  color: var(--ll-ink-muted);
  font: inherit;
  font-weight: 500;
  border-radius: 4px;
}

.breadcrumb-item:hover:not(:disabled) {
  color: var(--ll-accent);
}

.breadcrumb-item.active,
.breadcrumb-item:disabled {
  color: var(--ll-ink);
  font-weight: 600;
  cursor: default;
}

.separator {
  color: var(--ll-border);
  user-select: none;
}

.course-actions {
  display: flex;
  gap: 0.5rem;
  justify-content: flex-end;
  flex-wrap: wrap;
}

.course-btn {
  padding: 0.4rem 0.85rem;
  font-size: 0.85rem;
}

@media (max-width: 800px) {
  .course-bar {
    grid-template-columns: 1fr;
  }

  .search-container,
  .course-actions {
    justify-content: stretch;
  }

  .course-actions .course-btn {
    width: 100%;
  }
}
</style>
