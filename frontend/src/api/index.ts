import createClient from 'openapi-fetch';
import type {components, paths} from "@/api/schema.ts";
const client = createClient<paths>({ baseUrl: 'http://127.0.0.1:8000/api/' });
export default client;
export type schemas = components['schemas'];

export const getNodesList = async () => {
  const { data } = await client.GET('/nodes', {});
  return data;
};