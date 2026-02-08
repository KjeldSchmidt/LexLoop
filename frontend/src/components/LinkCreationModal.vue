<script lang="ts" setup>
import type { components } from '@/api/schema.ts'
import { onMounted, ref, watch } from 'vue'
import { addLink, getLinkTypes } from '@/api'
import SearchBar from '@/components/SearchBar.vue'
export type schemas = components['schemas']
type Node = schemas['NodeOut']
type Link = schemas['LinkOut']
type LinkTypeInfo = schemas['LinkTypeInfo']

const props = defineProps<{
  course_id: string
  show_modal: boolean
  node: Node
}>()

const emit = defineEmits<{
  (e: 'update:show_modal', value: boolean): void
  (e: 'confirm', result: { new_link: Link }): void
}>()

const linkTypes = ref<LinkTypeInfo[]>([])
const selectedLinkType = ref<string>('')
const selectedNode = ref<Node | null>(null)
const annotation = ref('')

const mutableCourseId = ref(props.course_id)

watch(
  () => props.course_id,
  (newValue) => {
    mutableCourseId.value = newValue
  },
)

function close() {
  selectedNode.value = null
  annotation.value = ''
  selectedLinkType.value = ''
  emit('update:show_modal', false)
}

onMounted(async () => {
  const res = await getLinkTypes()
  if (res != undefined && Array.isArray(res)) {
    linkTypes.value = res
    if (res.length > 0 && res[0] != undefined) {
      selectedLinkType.value = res[0].value
    }
  }
})

watch(
  () => props.show_modal,
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  async (newValue, _oldValue) => {
    if (newValue) {
      selectedNode.value = null
      annotation.value = ''
      const res = await getLinkTypes()
      if (res != undefined && Array.isArray(res)) {
        linkTypes.value = res
        if (res.length > 0 && res[0] != undefined) {
          selectedLinkType.value = res[0].value
        }
      }
    }
  },
)

function handleNodeSelect(result: { selected_node: Node }) {
  selectedNode.value = result.selected_node
}

async function confirm() {
  if (!selectedNode.value) {
    alert('Please select a second node')
    return
  }
  if (!selectedLinkType.value) {
    alert('Please select a link type')
    return
  }

  const new_link = await addLink({
    node1: props.node.uuid,
    node2: selectedNode.value.uuid,
    type: selectedLinkType.value,
    annotation: annotation.value,
  })

  if (new_link != undefined) {
    emit('confirm', { new_link: new_link })
    close()
  }
}
</script>

<template>
  <div v-if="show_modal" class="overlay" @click.self="close">
    <div class="modal">
      <header class="modal-header">
        New Link
        <button class="close" @click="close">×</button>
      </header>

      <section class="modal-body">
        <p>From Node: {{ node.term }}</p>

        <p>Link Type</p>
        <select v-model="selectedLinkType" class="link-type-select">
          <option v-for="linkType in linkTypes" :key="linkType.value" :value="linkType.value">
            {{ linkType.display_name }}
          </option>
        </select>

        <p>To Node</p>
        <SearchBar v-model:course_id="mutableCourseId" @select="handleNodeSelect" />
        <p v-if="selectedNode" class="selected-node">Selected: {{ selectedNode.term }}</p>

        <p>Annotation</p>
        <textarea v-model="annotation" name="annotation" rows="5" cols="33" />
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

.modal-body {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin: 1rem 0;
}

.modal-body p {
  margin: 0;
  font-weight: 500;
}

.link-type-select {
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 0.9rem;
  width: 100%;
}

.selected-node {
  color: #666;
  font-size: 0.9rem;
  font-weight: normal;
  font-style: italic;
}

textarea {
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 0.9rem;
  font-family: inherit;
  resize: vertical;
}
</style>
