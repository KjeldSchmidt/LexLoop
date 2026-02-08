<script setup lang="ts">
import { getLinksForNode, getLinkTypes, getNodeForUUID, getTagForUUID, updateNodeTags } from '@/api'
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { watch } from 'vue'
import type { components } from '@/api/schema.ts'
import TagUpdateModal from '@/components/TagUpdateModal.vue'
import HeaderBar from '@/components/HeaderBar.vue'
import { useNavigationHistoryStore } from '@/stores/navigationHistory'
import LinkCreationModal from '@/components/LinkCreationModal.vue'

export type schemas = components['schemas']

const show_tag_modal = ref(false)
const show_link_modal = ref(false)

type Node = schemas['NodeOut']
type Tag = schemas['TagOut']
type Link = schemas['LinkOut']
type LinkTypeInfo = schemas['LinkTypeInfo']
type LinkType = schemas['LinkType']

interface RelatedItem {
  uuid: string
  term: string
  type: LinkTypeInfo
}

const links = ref<RelatedItem[]>([])
const tags = ref<Tag[]>([])
const node = ref<Node>()
const linkTypes = ref<Set<LinkTypeInfo>>(new Set())
const activeFilters = ref<Set<LinkTypeInfo>>(new Set())

const route = useRoute()
const router = useRouter()
const navigationStore = useNavigationHistoryStore()

const id = route.params.id as string

const filteredLinks = computed(() => {
  return links.value.filter((link) => {
    for (const filterType of activeFilters.value) {
      if (filterType.value === link.type.value) {
        return true
      }
    }
    return false
  })
})

function toggleFilter(type: LinkTypeInfo) {
  if (activeFilters.value.has(type)) {
    activeFilters.value.delete(type)
  } else {
    activeFilters.value.add(type)
  }
  activeFilters.value = new Set(activeFilters.value)
}

function getLinkTypeInfo(type: LinkType) {
  for (const t of linkTypes.value) {
    if (type == t.value) return t
  }
  return undefined
}

async function update(id: string) {
  const res = await getNodeForUUID(id)

  if (res != undefined) {
    node.value = res
    navigationStore.pushPage({
      name: res.term,
      path: `/node/${id}`,
      type: 'node',
    })
    const res2 = await getLinksForNode(node.value.uuid)
    if (res2 != undefined && Array.isArray(res2)) {
      links.value = []
      for (const item of res2 as Link[]) {
        const link_type = getLinkTypeInfo(item.type)
        if (node.value.uuid == item.node1) {
          const other_node = await getNodeForUUID(item.node2)
          if (other_node != undefined && link_type != undefined)
            links.value.push({ uuid: other_node.uuid, term: other_node.term, type: link_type })
        } else {
          const other_node = await getNodeForUUID(item.node1)
          if (other_node != undefined && link_type != undefined)
            links.value.push({ uuid: other_node.uuid, term: other_node.term, type: link_type })
        }
      }
    }
    tags.value = []
    for (const item of node.value.tags) {
      const res = await getTagForUUID(item)
      if (res != undefined) tags.value.push(res as Tag)
    }
  }
}

async function handleTagsConfirm(result: { selected_tags: Tag[] }) {
  const new_tags = ref<string[]>([])
  for (const tag of result.selected_tags) {
    new_tags.value.push(tag.uuid)
  }

  if (node.value != undefined) {
    node.value = await updateNodeTags(node.value.uuid, new_tags.value)
    if (node.value != undefined) {
      tags.value = []
      for (const item of node.value.tags) {
        const res = await getTagForUUID(item)
        if (res != undefined) tags.value.push(res as Tag)
      }
    }
  }
}

async function handleLinksConfirm(result: { new_link: Link }) {
  //if (result.new_link != undefined) await update(id)
  //return
  if (result.new_link != undefined) {
    let other_id = result.new_link.node1
    if (id == other_id) other_id = result.new_link.node2
    const res = await getNodeForUUID(other_id)
    const link_type_info = getLinkTypeInfo(result.new_link.type)
    if (res != undefined && link_type_info != undefined)
      links.value.push({ uuid: res.uuid, term: res.term, type: link_type_info })
  }
}

function goToTag(tag: Tag) {
  router.push({ name: 'TagPage', params: { id: tag.uuid } })
}

function goToNode(item: RelatedItem) {
  router.push({ name: 'NodePage', params: { id: item.uuid } })
}

onMounted(async () => {
  const linkTypesList = await getLinkTypes()
  if (linkTypesList != undefined && Array.isArray(linkTypesList)) {
    linkTypes.value = new Set(linkTypesList)
    activeFilters.value = new Set(linkTypes.value)
  }
  await update(id)
})

watch(
  () => route.params.id,
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  async (newId, _oldId) => {
    links.value = []
    tags.value = []

    await update(newId as string)
  },
)
</script>

<template>
  <HeaderBar v-if="node" :course_id="node.course_uuid" />
  <div class="page-container">
    <div class="left-panel" v-if="node">
      <h2 class="word-title">{{ node.term }}</h2>
      <p class="word-definition">{{ node.definition }}</p>

      <div class="tags-section">
        <div class="tags-list">
          <button v-for="tag in tags" :key="tag.uuid" class="tag-pill" @click="goToTag(tag)">
            {{ tag.title }}
          </button>
          <button class="tag-pill add-btn" @click="show_tag_modal = true">+</button>
        </div>
      </div>
    </div>

    <div class="right-panel">
      <h2 class="panel-title">Related Things:</h2>

      <div class="links-list">
        <div
          v-for="item in filteredLinks"
          :key="item.uuid"
          class="link-item"
          @click="goToNode(item)"
        >
          {{ item.term }} ({{ item.type.display_name }})
        </div>
        <button class="add-link-btn" @click="show_link_modal = true">+</button>
      </div>

      <div class="filters-section">
        <label v-for="type in linkTypes" :key="type.value" class="filter-checkbox">
          <input type="checkbox" :checked="activeFilters.has(type)" @change="toggleFilter(type)" />
          {{ type.display_name }}
        </label>
      </div>
    </div>
  </div>

  <TagUpdateModal
    v-if="node"
    v-model:course_id="node.course_uuid"
    v-model:show_modal="show_tag_modal"
    v-model:tags="tags"
    @confirm="handleTagsConfirm"
  >
  </TagUpdateModal>

  <LinkCreationModal
    v-if="node"
    v-model:course_id="node.course_uuid"
    v-model:show_modal="show_link_modal"
    @confirm="handleLinksConfirm"
    v-model:node="node"
  >
  </LinkCreationModal>
</template>

<style scoped>
.page-container {
  display: flex;
  min-height: calc(100vh - 53px);
  background: #fff;
}

.left-panel {
  flex: 1;
  padding: 1.5rem;
  border-right: 1px solid #ccc;
  display: flex;
  flex-direction: column;
}

.right-panel {
  flex: 1;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
}

.word-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: #333;
}

.word-definition {
  color: #555;
  line-height: 1.5;
  margin-bottom: 1.5rem;
}

.tags-section {
  margin-bottom: 1.5rem;
}

.tags-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  align-items: center;
}

.tag-pill {
  padding: 0.5rem 1rem;
  border: 1px solid #333;
  border-radius: 20px;
  background: #fff;
  cursor: pointer;
  font-size: 0.85rem;
  transition: background-color 0.15s;
}

.tag-pill:hover {
  background-color: #f0f0f0;
}

.add-btn {
  width: 2rem;
  height: 2rem;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  border-radius: 50%;
}

.panel-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: #333;
}

.links-list {
  flex: 1;
}

.link-item {
  padding: 0.5rem 0;
  cursor: pointer;
  color: #333;
}

.link-item:hover {
  color: #666;
}

.add-link-btn {
  width: 2rem;
  height: 2rem;
  margin-top: 0.5rem;
  border: 1px solid #333;
  border-radius: 50%;
  background: #fff;
  cursor: pointer;
  font-size: 1.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.add-link-btn:hover {
  background-color: #f0f0f0;
}

.filters-section {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #ccc;
  margin-top: 1rem;
}

.filter-checkbox {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  cursor: pointer;
  font-size: 0.9rem;
}

.filter-checkbox input {
  cursor: pointer;
}
</style>
