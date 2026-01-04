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
  const { data } = await client.POST('/nodes/update/{node_uuid}/tags/' as any, {
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
