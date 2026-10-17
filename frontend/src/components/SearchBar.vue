<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { getNodesList } from '@/api'
import type { components } from '@/api/schema.ts'

type Node = components['schemas']['NodeOut']

const searchQuery = ref('')
const nodes = ref<Node[]>([])
const isOpen = ref(false)

const props = defineProps<{
  course_id: string
}>()

const emit = defineEmits<{
  (e: 'select', result: { selected_node: Node }): void
}>()

onMounted(async () => {
  const res = await getNodesList(props.course_id)
  if (res?.items) {
    nodes.value = res.items
  }
})

const filteredNodes = computed(() => {
  if (!searchQuery.value.trim()) {
    return []
  }

  const query = searchQuery.value.toLowerCase().trim()
  return nodes.value
    .filter((node) => {
      const termMatch = node.term.toLowerCase().includes(query)
      const definitionMatch = node.definition.toLowerCase().includes(query)
      return termMatch || definitionMatch
    })
    .slice(0, 10) // Limit to 10 results
})

function handleInput() {
  isOpen.value = searchQuery.value.trim().length > 0
}

function selectNode(node: Node) {
  emit('select', { selected_node: node })
  //router.push({ name: 'NodePage', params: { id: node.uuid } })
  searchQuery.value = ''
  isOpen.value = false
}

function handleBlur() {
  // Delay closing to allow click events to fire
  setTimeout(() => {
    isOpen.value = false
  }, 200)
}

function handleFocus() {
  if (searchQuery.value.trim().length > 0) {
    isOpen.value = true
  }
}
</script>

<template>
  <div class="search-container">
    <div class="search-input-wrapper">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Search nodes..."
        class="search-input"
        @input="handleInput"
        @focus="handleFocus"
        @blur="handleBlur"
      />
      <span class="search-icon" aria-hidden="true"></span>
    </div>

    <div v-if="isOpen && filteredNodes.length > 0" class="search-results">
      <div
        v-for="node in filteredNodes"
        :key="node.uuid"
        class="search-result-item"
        @mousedown.prevent="selectNode(node)"
      >
        <div class="result-term">{{ node.term }}</div>
        <div class="result-definition">{{ node.definition }}</div>
      </div>
    </div>

    <div
      v-if="isOpen && searchQuery.trim().length > 0 && filteredNodes.length === 0"
      class="search-results"
    >
      <div class="no-results">No nodes found</div>
    </div>
  </div>
</template>

<style scoped>
.search-container {
  position: relative;
  width: 100%;
  max-width: 500px;
}

.search-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.search-input {
  width: 100%;
  padding: 0.55rem 2.5rem 0.55rem 0.9rem;
  border: 1.5px solid var(--ll-border);
  border-radius: var(--ll-radius);
  background: var(--ll-surface);
  font-size: 0.9rem;
  outline: none;
  transition:
    border-color 0.15s ease,
    box-shadow 0.15s ease;
}

.search-input:focus {
  border-color: var(--ll-accent);
  box-shadow: 0 0 0 3px rgb(15 118 110 / 18%);
}

.search-icon {
  position: absolute;
  right: 0.85rem;
  width: 0.85rem;
  height: 0.85rem;
  border: 1.5px solid var(--ll-ink-muted);
  border-radius: 50%;
  pointer-events: none;
  opacity: 0.7;
}

.search-icon::after {
  content: '';
  position: absolute;
  width: 0.35rem;
  height: 1.5px;
  background: var(--ll-ink-muted);
  right: -0.3rem;
  bottom: -0.1rem;
  transform: rotate(45deg);
}

.search-results {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  margin-top: 0.35rem;
  background: var(--ll-surface);
  border: 1px solid var(--ll-border);
  border-radius: var(--ll-radius);
  box-shadow: var(--ll-shadow);
  max-height: 400px;
  overflow-y: auto;
  z-index: 1000;
}

.search-result-item {
  padding: 0.75rem 1rem;
  cursor: pointer;
  border-bottom: 1px solid var(--ll-paper-deep);
  transition: background-color 0.15s ease;
}

.search-result-item:last-child {
  border-bottom: none;
}

.search-result-item:hover {
  background-color: #f8fffd;
}

.result-term {
  font-weight: 600;
  color: var(--ll-ink);
  margin-bottom: 0.25rem;
}

.result-definition {
  font-size: 0.85rem;
  color: var(--ll-ink-muted);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.no-results {
  padding: 1rem;
  text-align: center;
  color: var(--ll-ink-muted);
  font-size: 0.9rem;
}
</style>
