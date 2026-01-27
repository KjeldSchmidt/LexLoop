<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { getNodesList } from '@/api'
import type { components } from '@/api/schema.ts'

type Node = components['schemas']['NodeOut']

const searchQuery = ref('')
const nodes = ref<Node[]>([])
const isOpen = ref(false)

const emit = defineEmits<{
  (e: 'select', result: { selected_node: Node }): void
}>()

onMounted(async () => {
  const res = await getNodesList()
  if (res != undefined && Array.isArray(res)) {
    nodes.value = res
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
      <span class="search-icon">🔍</span>
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
  padding: 0.5rem 2.5rem 0.5rem 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 0.9rem;
  outline: none;
  transition: border-color 0.2s;
}

.search-input:focus {
  border-color: #333;
}

.search-icon {
  position: absolute;
  right: 0.75rem;
  pointer-events: none;
  font-size: 1rem;
}

.search-results {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  margin-top: 0.25rem;
  background: white;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  max-height: 400px;
  overflow-y: auto;
  z-index: 1000;
}

.search-result-item {
  padding: 0.75rem 1rem;
  cursor: pointer;
  border-bottom: 1px solid #f0f0f0;
  transition: background-color 0.15s;
}

.search-result-item:last-child {
  border-bottom: none;
}

.search-result-item:hover {
  background-color: #f5f5f5;
}

.result-term {
  font-weight: 500;
  color: #333;
  margin-bottom: 0.25rem;
}

.result-definition {
  font-size: 0.85rem;
  color: #666;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.no-results {
  padding: 1rem;
  text-align: center;
  color: #999;
  font-size: 0.9rem;
}
</style>
