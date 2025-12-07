<script setup lang="ts">
import { getTagsList } from '@/api'
import { ref, onMounted } from 'vue'

const tags = ref([] as any)
let first_tag = ref()

onMounted(async () => {
  const res = await getTagsList()

  if (res != undefined && Array.isArray(res)) {
    tags.value = res
    first_tag.value = tags.value[0]
  }
})
</script>

<template>
  <RouterLink v-if="first_tag" :to="{ name: 'TagPage', params: { id: first_tag.uuid } }">
    <button>Choose Course</button>
  </RouterLink>
</template>

<style scoped></style>
