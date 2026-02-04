import type { Handle } from "@sveltejs/kit";
import { client } from "$lib/openapiClient";

const apiClientHandle: Handle = async ({ event, resolve }) => {
  event.locals.client = client;
  return await resolve(event);
}

export default apiClientHandle;