<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getTagsList, getNodesList } from '@/api'
import { useRouter } from 'vue-router'
import type { components } from '@/api/schema.ts'
import HeaderBar from '@/components/HeaderBar.vue'
import { useNavigationHistoryStore } from '@/stores/navigationHistory'
import NodeCreationModal from '@/components/NodeCreationModal.vue'
import TagCreationModal from '@/components/TagCreationModal.vue'

type Tag = components['schemas']['TagOut']
type Node = components['schemas']['NodeOut']

const router = useRouter()
const tags = ref<Tag[]>([])
const nodes = ref<Node[]>([])
const navigationStore = useNavigationHistoryStore()
const show_node_modal = ref(false)
const show_tag_modal = ref(false)

onMounted(async () => {
  navigationStore.resetToClass('Class')

  const [tagsRes, nodesRes] = await Promise.all([getTagsList(), getNodesList()])

  if (tagsRes && Array.isArray(tagsRes)) {
    tags.value = tagsRes
  }
  if (nodesRes && Array.isArray(nodesRes)) {
    nodes.value = nodesRes
  }
})

function goToTag(tag: Tag) {
  router.push({ name: 'TagPage', params: { id: tag.uuid } })
}

function goToNode(node: Node) {
  router.push({ name: 'NodePage', params: { id: node.uuid } })
}

async function handleNodeCreation(result: { new_node: Node }) {
  if (result.new_node != undefined) nodes.value.push(result.new_node)
}

async function handleTagCreation(result: { new_tag: Tag }) {
  if (result.new_tag != undefined) tags.value.push(result.new_tag)
}
</script>

<template>
  <HeaderBar />
  <div class="book-container">
    <div class="page left-page">
      <h2 class="page-title">All Tags</h2>
      <div class="card-grid">
        <button v-for="tag in tags" :key="tag.uuid" class="card" @click="goToTag(tag)">
          {{ tag.title }}
        </button>
      </div>
      <button class="fab" @click="show_tag_modal = true">+</button>
    </div>

    <div class="page right-page">
      <h2 class="page-title">All Words</h2>
      <div class="card-grid">
        <button v-for="node in nodes" :key="node.uuid" class="card" @click="goToNode(node)">
          {{ node.term }}
        </button>
      </div>
      <button class="fab" @click="show_node_modal = true">+</button>
    </div>
  </div>

  <NodeCreationModal v-model:show_modal="show_node_modal" @confirm="handleNodeCreation">
  </NodeCreationModal>
  <TagCreationModal v-model:show_modal="show_tag_modal" @confirm="handleTagCreation">
  </TagCreationModal>
</template>

<style scoped>
.fab {
  position: fixed;
  bottom: 2rem;
  width: 3rem;
  height: 3rem;
  border-radius: 50%;
  border: 2px solid #333;
  background: #fff;
  font-size: 1.5rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.book-container {
  display: flex;
  min-height: calc(100vh - 53px);
  background: #fff;
}

.page {
  flex: 1;
  padding: 1.5rem;
  overflow-y: auto;
}

.left-page {
  border-right: 1px solid #ccc;
}

.page-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: #333;
}

.card-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.75rem;
}

.card {
  padding: 0.75rem 1rem;
  border: 1px solid #333;
  border-radius: 20px;
  background: #fff;
  cursor: pointer;
  font-size: 0.9rem;
  text-align: center;
  transition: background-color 0.15s;
}

.card:hover {
  background-color: #f0f0f0;
}
</style>
