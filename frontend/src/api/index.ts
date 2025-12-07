import createClient from 'openapi-fetch'
import type { components, paths } from '@/api/schema.ts'
const client = createClient<paths>({ baseUrl: 'http://127.0.0.1:8000/api/' })
export default client
export type schemas = components['schemas']

export const getNodesList = async () => {
  const { data } = await client.GET('/nodes', {})
  return data
}

export const getTagsList = async () => {
  const { data } = await client.GET('/tags', {})
  return data
}

export const getLinksForNode = async (node_uuid: string) => {
  const { data } = await client.GET('/nodes/{id}/links', {
    params: {
      path: { id: node_uuid },
    },
  })
  return data
}

export const getNodeForUUID = async (node_uuid: string) => {
  const { data } = await client.GET('/nodes/{id}', {
    params: {
      path: { id: node_uuid },
    },
  })
  return data
}

export const getTagForUUID = async (tag_uuid: string) => {
  const { data } = await client.GET('/tags/{id}', {
    params: {
      path: { id: tag_uuid },
    },
  })
  return data
}

export const getNodesForTag = async (tag_uuid: string) => {
  const { data } = await client.GET('/nodes/tag/{id}', {
    params: {
      path: { id: tag_uuid },
    },
  })
  return data
}

export const getTagsForNodeUUID = async (node_uuid: string) => {
  const { data } = await client.GET('/tags/node/{id}', {
    params: {
      path: { id: node_uuid },
    },
  })
  return data
}
