<script setup lang="ts">
import { defineProps } from 'vue'
import { useRouter } from 'vue-router'
import type { components } from '@/api/schema.ts'
export type schemas = components['schemas']

type Tag = schemas['TagOut']

const router = useRouter()

// Define the props for the component
defineProps<{
  title: string
  definition: string
  tags: Tag[]
}>()

function handleClick(item: Tag) {
  router.push({
    name: 'TagPage',
    params: { id: item.uuid },
  })
}
</script>

<template>
  <div>
    <p>{{ title }}</p>
    <p>{{ definition }}</p>
  </div>
  <div>
    <h3>Tags</h3>
    <ul>
      <li v-for="item in tags" :key="item.uuid" @click="handleClick(item)">
        {{ item.title }}
      </li>
    </ul>
  </div>
</template>

<style scoped></style>
