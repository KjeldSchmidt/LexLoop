<script setup lang="ts">
import NodeCard from '@/components/NodeCard.vue'
import {getNodesList} from "@/api";
import { ref, onMounted } from 'vue'

const nodes = ref([] as any)

onMounted(async () => {
  const res = await getNodesList()

  if (res != undefined)
    nodes.value = res;
})
</script>

<template>
  <h1>Willkommen!</h1>
  <div>
    <NodeCard :title="item.term" :definition="item.definition"  v-for="item in nodes" :key="item.uuid"> </NodeCard>
  </div>
</template>

<style scoped></style>
