<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router'
import { addNode, getNodesForTag, getTagForUUID } from '@/api'
import { onMounted, ref } from 'vue'
import TagCard from '@/components/TagCard.vue'
import type { components } from '@/api/schema.ts'
import NodeCreationModal from '@/components/NodeCreationModal.vue'
export type schemas = components['schemas']

type Node = schemas['NodeOut']
type NodeIn = schemas['NodeIn']
type Tag = schemas['TagOut']

const show_modal = ref(false)

const route = useRoute()
const tag_nodes = ref<Node[]>()
const tag = ref<Tag>()

const id = route.params.id as string

const router = useRouter()

onMounted(async () => {
  const res = await getTagForUUID(id)

  if (res != undefined) {
    tag.value = res
    const res2 = await getNodesForTag(tag.value.uuid)
    if (res2 != undefined && Array.isArray(res2)) {
      tag_nodes.value = res2
    }
  }
})

function handleClick(item: Node) {
  console.log(item.term)

  router.push({
    name: 'NodePage',
    params: { id: item.uuid },
  })
}

async function handleNodeCreation(result: { new_node: NodeIn }) {
  const new_node = await addNode(result.new_node)
  if (new_node != undefined)
    await router.push({
      name: 'NodePage',
      params: { id: new_node.uuid },
    })
}
</script>

<template>
  <div class="page">
    <div class="left-column">
      <TagCard :title="tag.title" :description="tag.description" v-if="tag"></TagCard>
    </div>

    <div class="right-column">
      <ul>
        <li v-for="item in tag_nodes" :key="item.uuid" @click="handleClick(item)">
          {{ item.term }}
        </li>
      </ul>
    </div>
  </div>

  <button @click="show_modal = true">New Node</button>

  <NodeCreationModal v-model:show_modal="show_modal" @confirm="handleNodeCreation">
  </NodeCreationModal>
</template>

<style scoped>
.page {
  display: flex;
  flex-direction: row;
  gap: 16px;
}

.left-column {
  column-width: 250px;
}
</style>
