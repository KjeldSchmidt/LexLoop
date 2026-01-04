<script lang="ts" setup>
import type { components } from '@/api/schema.ts'
import { onMounted, ref, watch } from 'vue'
import { getTagsList } from '@/api'
export type schemas = components['schemas']
type Tag = schemas['TagOut']

const props = defineProps<{
  show_modal: boolean
  tags: Tag[]
}>()

const selected_tags = ref<Tag[]>([...props.tags])
const all_tags = ref<Tag[]>([])

const emit = defineEmits<{
  (e: 'update:show_modal', value: boolean): void
  (e: 'confirm', result: { selected_tags: Tag[] }): void
}>()

function close() {
  emit('update:show_modal', false)
}

function onToggle(item: Tag, event: Event) {
  const checked = (event.target as HTMLInputElement).checked

  if (checked) {
    selected_tags.value.push(item)
  } else {
    const num = selected_tags.value.findIndex((i) => i.uuid == item.uuid)
    selected_tags.value.splice(num, 1)
  }
}

onMounted(async () => {
  const res = await getTagsList()

  if (res != undefined && Array.isArray(res)) {
    all_tags.value = res
  }
})

watch(
  () => props.show_modal,
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  (newValue, _oldValue) => {
    if (newValue) {
      selected_tags.value = [...props.tags]
    }
  },
)

function confirm() {
  emit('confirm', { selected_tags: selected_tags.value })
  emit('update:show_modal', false)
}
</script>

<template>
  <div v-if="show_modal" class="overlay" @click.self="close">
    <div class="modal">
      <header class="modal-header">
        Choose Tags
        <button class="close" @click="close">×</button>
      </header>

      <section class="modal-body">
        <ul>
          <li v-for="item in all_tags" :key="item.uuid">
            {{ item.title }}
            <input
              type="checkbox"
              :value="item"
              :checked="selected_tags.findIndex((i) => i.uuid == item.uuid) != -1"
              @change="onToggle(item, $event)"
            />
          </li>
        </ul>
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
