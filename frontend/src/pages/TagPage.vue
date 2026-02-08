<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router'
import { getNodesForTag, getTagForUUID } from '@/api'
import { onMounted, ref } from 'vue'
import type { components } from '@/api/schema.ts'
import NodeCreationModal from '@/components/NodeCreationModal.vue'
import HeaderBar from '@/components/HeaderBar.vue'
import { useNavigationHistoryStore } from '@/stores/navigationHistory'

export type schemas = components['schemas']

type NodeOut = schemas['NodeOut']
type Tag = schemas['TagOut']

const show_modal = ref(false)

const route = useRoute()
const tag_nodes = ref<NodeOut[]>()
const tag = ref<Tag>()
const tags = ref<Tag[]>([])

const id = route.params.id as string

const router = useRouter()
const navigationStore = useNavigationHistoryStore()

onMounted(async () => {
  const res = await getTagForUUID(id)

  if (res != undefined) {
    tag.value = res
    navigationStore.pushPage({
      name: res.title,
      path: `/tag/${id}`,
      type: 'tag',
    })
    tags.value.push(tag.value)
    const res2 = await getNodesForTag(tag.value.uuid)
    if (res2 != undefined && Array.isArray(res2)) {
      tag_nodes.value = res2
    }
  }
})

function handleClick(item: NodeOut) {
  router.push({
    name: 'NodePage',
    params: { id: item.uuid },
  })
}

async function handleNodeCreation(result: { new_node: NodeOut }) {
  if (result.new_node != undefined)
    await router.push({
      name: 'NodePage',
      params: { id: result.new_node.uuid },
    })
}
</script>

<template>
  <HeaderBar v-if="tag" :course_id="tag.course_uuid" />
  <div class="page-container">
    <div class="left-panel" v-if="tag">
      <h2 class="tag-title">{{ tag.title }}</h2>
      <p class="tag-description">{{ tag.description }}</p>
    </div>

    <div class="right-panel">
      <h2 class="panel-title">Words in Tag</h2>
      <div class="card-grid">
        <button v-for="item in tag_nodes" :key="item.uuid" class="card" @click="handleClick(item)">
          {{ item.term }}
        </button>
      </div>
    </div>

    <button class="fab" @click="show_modal = true">+</button>
  </div>

  <NodeCreationModal
    v-if="tag"
    v-model:course_id="tag.course_uuid"
    v-model:show_modal="show_modal"
    v-model:tags="tags"
    @confirm="handleNodeCreation"
  >
  </NodeCreationModal>
</template>

<style scoped>
.page-container {
  display: flex;
  min-height: calc(100vh - 53px);
  background: #fff;
  position: relative;
}

.left-panel {
  flex: 1;
  padding: 1.5rem;
  border-right: 1px solid #ccc;
}

.right-panel {
  flex: 1;
  padding: 1.5rem;
  overflow-y: auto;
}

.tag-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: #333;
}

.tag-description {
  color: #555;
  line-height: 1.5;
}

.panel-title {
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

.fab {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
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

.fab:hover {
  background-color: #f0f0f0;
}
</style>
