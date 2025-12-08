<script setup lang="ts">
import NodeCard from '@/components/NodeCard.vue'
import { getLinksForNode, getNodeForUUID, getTagForUUID } from '@/api'
import { ref, onMounted } from 'vue'
import LinksList from '@/components/LinksList.vue'
import type { ListItem } from '@/components/LinksList.vue'
import { useRoute } from 'vue-router'
import { watch } from 'vue'
import type { components } from '@/api/schema.ts'
export type schemas = components['schemas']

type Node = schemas['NodeOut']
type Tag = schemas['TagOut']

const links = ref<ListItem[]>([])
const tags = ref<Tag[]>([])
const node = ref<Node>()

const route = useRoute()

const id = route.params.id as string

async function update(id: string) {
  const res = await getNodeForUUID(id)

  if (res != undefined) {
    node.value = res
    const res2 = await getLinksForNode(node.value.uuid)
    if (res2 != undefined && Array.isArray(res2)) {
      for (const item of res2) {
        if (node.value.uuid == item.node1) {
          const other_node = await getNodeForUUID(item.node2)
          if (other_node != undefined)
            links.value.push({ uuid: other_node.uuid, title: other_node.term })
        } else {
          const other_node = await getNodeForUUID(item.node1)
          if (other_node != undefined)
            links.value.push({ uuid: other_node.uuid, title: other_node.term })
        }
      }
    }
    for (const item of node.value.tags) {
      const res = await getTagForUUID(item)
      if (res != undefined) tags.value.push(res as Tag)
    }
  }
}

onMounted(async () => {
  await update(id)
})

watch(
  () => route.params.id,
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  async (newId, _oldId) => {
    links.value = []
    tags.value = []

    await update(newId as string)
  },
)
</script>

<template>
  <div class="page">
    <div class="left-column">
      <NodeCard
        :title="node.term"
        :definition="node.definition"
        :key="node.uuid"
        :tags="tags"
        v-if="node"
      ></NodeCard>
    </div>

    <div class="right-column">
      <h2>Links</h2>
      <LinksList :items="links" />
    </div>
  </div>
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
