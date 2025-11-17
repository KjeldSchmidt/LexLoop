<script setup lang="ts">
import { defineProps } from 'vue'

defineProps({
  title: {
    type: String,
    required: true,
  },
  definition: {
    type: String,
    required: true,
  },
})
</script>

<template>
  <div>
    <p>{{ title }}</p>
    <p>{{ definition }}</p>
  </div>
</template>

<style scoped>
p {
  color: red;
}
</style>
