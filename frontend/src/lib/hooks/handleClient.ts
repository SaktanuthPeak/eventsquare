import type { Handle } from "@sveltejs/kit";
import { createClient } from "@hey-api/client-fetch";
import { env } from "$env/dynamic/private";

export const handleFetchClient: Handle = async ({ event, resolve }) => {
    const token = event.cookies.get('access_token')
    const headers: HeadersInit = {}
    if (token) {
        headers["Authorization"] = `Bearer ${token}`
    }
    event.locals.client = createClient({
        baseUrl: env.API_URL,
        headers: headers
    })
    return await resolve(event);
}