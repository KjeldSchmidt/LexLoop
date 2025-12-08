<script setup lang="ts">
import { defineProps } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// Define the type for the item
export type ListItem = {
  uuid: string
  title: string
}

// Define the props for the component
defineProps<{
  items: ListItem[]
}>()

function handleClick(item: ListItem) {
  router.push({
    name: 'NodePage',
    params: { id: item.uuid },
  })
}
</script>

<template>
  <ul>
    <li v-for="item in items" :key="item.uuid" @click="handleClick(item)">
      {{ item.title }}
    </li>
  </ul>
</template>

<style scoped></style>
