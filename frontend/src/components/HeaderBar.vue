<script setup lang="ts">
import { useNavigationHistoryStore } from '@/stores/navigationHistory'
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import SearchBar from '@/components/SearchBar.vue'
import type { components } from '@/api/schema.ts'

type Node = components['schemas']['NodeOut']

const store = useNavigationHistoryStore()
const { history } = storeToRefs(store)
const router = useRouter()

function goTo(path: string) {
  router.push(path)
}

function goToClasses() {
  router.push('/class')
}

function handleSelect(result: { selected_node: Node }) {
  router.push({ name: 'NodePage', params: { id: result.selected_node.uuid } })
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

    <div class="header-actions">
      <SearchBar @select="handleSelect" />
    </div>

    <div class="header-actions">
      <button class="header-btn" @click="goToClasses">Back to Classes</button>
      <button class="header-btn">Profile</button>
    </div>
  </header>
</template>

<style scoped>
.header-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1.5rem;
  border-bottom: 1px solid #ccc;
  background: #fff;
}

.breadcrumbs {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
}

.breadcrumb-item {
  cursor: pointer;
  color: #555;
}

.breadcrumb-item:hover {
  color: #000;
}

.breadcrumb-item.active {
  color: #000;
  font-weight: 500;
}

.separator {
  color: #999;
}

.header-actions {
  display: flex;
  gap: 0.5rem;
}

.header-btn {
  padding: 0.5rem 1rem;
  border: 1px solid #333;
  border-radius: 4px;
  background: #fff;
  cursor: pointer;
  font-size: 0.85rem;
}

.header-btn:hover {
  background: #f0f0f0;
}
</style>
