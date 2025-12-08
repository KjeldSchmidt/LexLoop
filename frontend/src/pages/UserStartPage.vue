<script setup lang="ts">
import { getTagsList } from '@/api'
import { ref, onMounted } from 'vue'
import type { components } from '@/api/schema.ts'
export type schemas = components['schemas']

type Tag = schemas['TagOut']
let tags: Tag[]
const first_tag = ref<Tag>()

onMounted(async () => {
  const res = await getTagsList()

  if (res != undefined && Array.isArray(res) && res.length != 0) {
    tags = res
    first_tag.value = tags[0]
  }
})
</script>

<template>
  <RouterLink v-if="first_tag" :to="{ name: 'TagPage', params: { id: first_tag.uuid } }">
    <button>Choose Course</button>
  </RouterLink>
</template>

<style scoped></style>
