<script setup lang="ts">
import NodeCard from '@/components/NodeCard.vue'
import { getLinksForNode, getNodeForUUID, getNodesList, getTagForUUID } from '@/api'
import { ref, onMounted } from 'vue'
import LinksList from '@/components/LinksList.vue'
import { useRoute } from 'vue-router'
import { watch } from 'vue'

const links = ref([] as any)
let node = ref()

const route = useRoute()

const id = route.params.id as string

onMounted(async () => {
  const res = await getNodeForUUID(id)

  if (res != undefined) {
    node.value = res
  }

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
})

watch(
  () => route.params.id,
  async (newId, oldId) => {
    const res = await getNodeForUUID(newId)

    links.value = []

    if (res != undefined) {
      node.value = res
    }

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
