<script lang="ts" setup>
import type { components } from '@/api/schema.ts'
import { onMounted, watch } from 'vue'
import { addTag } from '@/api'
export type schemas = components['schemas']
type TagOut = schemas['TagOut']

const props = defineProps<{
  show_modal: boolean
}>()

const emit = defineEmits<{
  (e: 'update:show_modal', value: boolean): void
  (e: 'confirm', result: { new_tag: TagOut }): void
}>()

function close() {
  emit('update:show_modal', false)
}

onMounted(async () => {})

watch(
  () => props.show_modal,
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  (_newValue, _oldValue) => {},
)

async function confirm() {
  const new_tag = await addTag({
    title: (document.getElementById('title') as HTMLInputElement).value,
    description: (document.getElementById('description') as HTMLInputElement).value,
  })

  if (new_tag != undefined) emit('confirm', { new_tag: new_tag })
  emit('update:show_modal', false)
}
</script>

<template>
  <div v-if="show_modal" class="overlay" @click.self="close">
    <div class="modal">
      <header class="modal-header">
        New Tag
        <button class="close" @click="close">×</button>
      </header>

      <section class="modal-body">
        <p>Title</p>
        <input type="text" id="title" />
        <p>Description</p>
        <textarea id="description" name="description" rows="5" cols="33" />
      </section>

      <footer class="modal-footer">
        <button @click="confirm">Confirm</button>
      </footer>
    </div>
  </div>
</template>

<style scoped>
.overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal {
  background: white;
  width: 400px;
  border-radius: 8px;
  padding: 1rem;
}

.close {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
}

.modal-header,
.modal-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
