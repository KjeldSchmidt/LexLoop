<script setup lang="ts">
import NodeCard from '@/components/NodeCard.vue'
import { getLinksForNode, getNodeForUUID } from '@/api'
import { ref, onMounted } from 'vue'
import LinksList from '@/components/LinksList.vue'
import type { ListItem } from '@/components/LinksList.vue'
import { useRoute } from 'vue-router'
import { watch } from 'vue'
import type { components } from '@/api/schema.ts'
export type schemas = components['schemas']

type Node = schemas['NodeOut']

const links = ref<ListItem[]>([])
const node = ref<Node>()

const route = useRoute()

const id = route.params.id as string

onMounted(async () => {
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
  }
})

watch(
  () => route.params.id,
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  async (newId, _oldId) => {
    const res = await getNodeForUUID(newId as string)

    links.value = []

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
    }
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
