import createClient from 'openapi-fetch'
import type { components, paths } from '@/api/schema.ts'
const client = createClient<paths>({ baseUrl: import.meta.env.VITE_API_URL })
export default client
export type schemas = components['schemas']
type NodeIn = schemas['NodeIn']
type TagIn = schemas['TagIn']
type LinkIn = schemas['LinkIn']

export const getNodesList = async (course_uuid: string) => {
  const { data } = await client.GET(`/course/{course_uuid}/nodes`, {
    params: {
      path: { course_uuid: course_uuid },
    },
  })
  return data
}

export const getTagsList = async (course_uuid: string) => {
  const { data } = await client.GET(`/course/{course_uuid}/tags`, {
    params: {
      path: { course_uuid: course_uuid },
    },
  })
  return data
}

export const getLinksForNode = async (node_uuid: string) => {
  const { data } = await client.GET('/nodes/{node_uuid}/links', {
    params: {
      path: { node_uuid: node_uuid },
    },
  })
  return data
}

export const getNodeForUUID = async (node_uuid: string) => {
  const { data } = await client.GET('/nodes/{uuid}', {
    params: {
      path: { uuid: node_uuid },
    },
  })
  return data
}

export const getTagForUUID = async (tag_uuid: string) => {
  const { data } = await client.GET('/tags/{uuid}', {
    params: {
      path: { uuid: tag_uuid },
    },
  })
  return data
}

export const getNodesForTag = async (tag_uuid: string) => {
  const { data } = await client.GET('/nodes/tag/{tag_uuid}', {
    params: {
      path: { tag_uuid: tag_uuid },
    },
  })
  return data
}

export const getTagsForNodeUUID = async (node_uuid: string) => {
  const { data } = await client.GET('/tags/node/{node_uuid}', {
    params: {
      path: { node_uuid: node_uuid },
    },
  })
  return data
}

export const addTagToNode = async (node_uuid: string, tag_uuid: string) => {
  await client.POST('/nodes/{node_uuid}/{tag_uuid}', {
    params: {
      path: {
        node_uuid: node_uuid,
        tag_uuid: tag_uuid,
      },
    },
  })
}

export const updateNodeTags = async (node_uuid: string, tag_uuids: string[]) => {
  const { data } = await client.POST('/nodes/update/{node_uuid}/tags/', {
    params: {
      path: {
        node_uuid: node_uuid,
      },
    },
    body: {
      tag_uuids: tag_uuids,
    },
  })
  return data
}

export const addNode = async (node: NodeIn) => {
  const { data } = await client.POST('/nodes', {
    body: {
      node: node,
    },
  })
  return data
}

export const addTag = async (tag: TagIn) => {
  const { data } = await client.POST('/tags', {
    body: {
      tag: tag,
    },
  })
  return data
}

export const addLink = async (link: LinkIn) => {
  const { data } = await client.POST('/links', {
    body: {
      link: link,
    },
  })
  return data
}

export const getLinkTypes = async () => {
  const { data } = await client.GET('/links/types', {})
  return data
}

export const getCourses = async () => {
  const { data } = await client.GET('/courses', {})
  return data
}
