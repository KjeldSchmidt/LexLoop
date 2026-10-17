<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getTagsList, getNodesList } from '@/api'
import { useRoute, useRouter } from 'vue-router'
import type { components } from '@/api/schema.ts'
import HeaderBar from '@/components/HeaderBar.vue'
import { useNavigationHistoryStore } from '@/stores/navigationHistory'
import NodeCreationModal from '@/components/NodeCreationModal.vue'
import TagCreationModal from '@/components/TagCreationModal.vue'

type Tag = components['schemas']['TagOut']
type Node = components['schemas']['NodeOut']

const route = useRoute()
const course_id = route.params.id as string

const router = useRouter()
const tags = ref<Tag[]>([])
const nodes = ref<Node[]>([])
const navigationStore = useNavigationHistoryStore()
const show_node_modal = ref(false)
const show_tag_modal = ref(false)

onMounted(async () => {
  navigationStore.resetToClass('Class', course_id)
  const [tagsRes, nodesRes] = await Promise.all([getTagsList(course_id), getNodesList(course_id)])

  if (tagsRes?.items) {
    tags.value = tagsRes.items
  }
  if (nodesRes?.items) {
    nodes.value = nodesRes.items
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
  <HeaderBar :course_id="course_id" />
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

  <NodeCreationModal
    v-model:course_id="course_id"
    v-model:show_modal="show_node_modal"
    @confirm="handleNodeCreation"
  >
  </NodeCreationModal>
  <TagCreationModal
    v-model:course_uuid="course_id"
    v-model:show_modal="show_tag_modal"
    @confirm="handleTagCreation"
  >
  </TagCreationModal>
</template>

<style scoped>
.fab {
  position: fixed;
  bottom: 2rem;
  width: 3.25rem;
  height: 3.25rem;
  border-radius: 50%;
  border: none;
  background: var(--ll-accent);
  color: #fff;
  font-size: 1.6rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: var(--ll-shadow);
  transition:
    background-color 0.15s ease,
    transform 0.15s ease;
}

.fab:hover {
  background: var(--ll-accent-hover);
  transform: scale(1.05);
}

.left-page .fab {
  left: 1.5rem;
}

.right-page .fab {
  right: 1.5rem;
}

.book-container {
  display: flex;
  min-height: calc(100vh - 57px);
  background: rgb(255 255 255 / 55%);
  backdrop-filter: blur(4px);
}

.page {
  flex: 1;
  padding: 1.5rem var(--ll-space-page);
  overflow-y: auto;
  position: relative;
}

.left-page {
  border-right: 1px solid var(--ll-border);
}

.page-title {
  font-family: var(--ll-font-display);
  font-size: 1.35rem;
  font-weight: 600;
  margin-bottom: 1.1rem;
  color: var(--ll-ink);
}

.card-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.75rem;
}

.card {
  padding: 0.8rem 1rem;
  border: 1.5px solid var(--ll-border);
  border-radius: var(--ll-radius-pill);
  background: var(--ll-surface);
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 500;
  text-align: center;
  transition:
    background-color 0.15s ease,
    border-color 0.15s ease,
    transform 0.15s ease;
}

.card:hover {
  background: #f8fffd;
  border-color: var(--ll-accent);
  transform: translateY(-1px);
}

@media (max-width: 720px) {
  .book-container {
    flex-direction: column;
  }

  .left-page {
    border-right: none;
    border-bottom: 1px solid var(--ll-border);
  }

  .left-page .fab,
  .right-page .fab {
    left: auto;
    right: 1.25rem;
  }

  .left-page .fab {
    bottom: auto;
    top: calc(100% - 4.5rem);
  }
}
</style>
