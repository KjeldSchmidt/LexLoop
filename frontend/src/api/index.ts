import createClient from 'openapi-fetch'
import type { components, paths } from '@/api/schema.ts'
const client = createClient<paths>({
  baseUrl: import.meta.env.VITE_API_URL,
  credentials: 'include',
})
export default client
export type schemas = components['schemas']
type NodeIn = schemas['NodeIn']
type TagIn = schemas['TagIn']
type LinkIn = schemas['LinkIn']

/** Max page size allowed by the API; use for UI that still wants a full first page. */
export const API_MAX_PAGE_SIZE = 100

type PageParams = { offset?: number; limit?: number }

export const getNodesList = async (
  course_uuid: string,
  { offset = 0, limit = API_MAX_PAGE_SIZE }: PageParams = {},
) => {
  const { data } = await client.GET(`/course/{course_uuid}/nodes`, {
    params: {
      path: { course_uuid: course_uuid },
      query: { offset, limit },
    },
  })
  return data
}

export const getTagsList = async (
  course_uuid: string,
  { offset = 0, limit = API_MAX_PAGE_SIZE }: PageParams = {},
) => {
  const { data } = await client.GET(`/course/{course_uuid}/tags`, {
    params: {
      path: { course_uuid: course_uuid },
      query: { offset, limit },
    },
  })
  return data
}

export const getLinksForNode = async (
  node_uuid: string,
  { offset = 0, limit = API_MAX_PAGE_SIZE }: PageParams = {},
) => {
  const { data } = await client.GET('/nodes/{node_uuid}/links', {
    params: {
      path: { node_uuid: node_uuid },
      query: { offset, limit },
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

export const getNodesForTag = async (
  tag_uuid: string,
  { offset = 0, limit = API_MAX_PAGE_SIZE }: PageParams = {},
) => {
  const { data } = await client.GET('/nodes/tag/{tag_uuid}', {
    params: {
      path: { tag_uuid: tag_uuid },
      query: { offset, limit },
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

export const getCourses = async ({ offset = 0, limit = API_MAX_PAGE_SIZE }: PageParams = {}) => {
  const { data } = await client.GET('/courses', {
    params: {
      query: { offset, limit },
    },
  })
  return data
}

export const getGoogleAuthorizeUrl = async () => {
  const { data, error } = await client.GET('/auth/google/authorize')
  if (error || !data?.authorization_url) {
    throw new Error('GOOGLE_AUTHORIZE_FAILED')
  }
  return data.authorization_url
}

export const getTeacherMe = async () => {
  const { data, error } = await client.GET('/auth/users/me')
  if (error || !data) {
    return null
  }
  return data
}

export const getStudentMe = async () => {
  const { data, error } = await client.GET('/students/me')
  if (error || !data) {
    return null
  }
  return data
}

export const teacherLogout = async () => {
  await client.POST('/auth/logout', {})
}

export const studentLogin = async (username: string, password: string) => {
  const { data, error } = await client.POST('/students/login', {
    body: { username, password },
  })
  if (error) {
    throw new Error('LOGIN_FAILED')
  }
  return data
}

export const studentLogout = async () => {
  await client.POST('/students/logout', {})
}

export const getStudents = async () => {
  const { data } = await client.GET('/students', {})
  return data
}

export const createStudent = async (username: string, password: string) => {
  const { data, error } = await client.POST('/students', {
    body: { username, password },
  })
  if (error) {
    throw new Error('CREATE_FAILED')
  }
  return data
}

export const bulkCreateStudents = async (count: number) => {
  const { data, error } = await client.POST('/students/bulk', {
    body: { count },
  })
  if (error) {
    throw new Error('BULK_CREATE_FAILED')
  }
  return data
}

export const bulkDeleteStudents = async (student_uuids: string[]) => {
  const { error } = await client.POST('/students/bulk-delete', {
    body: { student_uuids },
  })
  if (error) {
    throw new Error('BULK_DELETE_FAILED')
  }
}

export const bulkResetStudentPasswords = async (student_uuids: string[]) => {
  const { data, error } = await client.POST('/students/bulk-passwords', {
    body: { student_uuids },
  })
  if (error) {
    throw new Error('BULK_PASSWORD_RESET_FAILED')
  }
  return data
}
