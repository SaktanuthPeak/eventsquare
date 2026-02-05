import { getEvents, type EventResponse } from '$lib/client';
import type { PageServerLoad } from './$types';
import { env } from '$env/dynamic/private';
export const load = (async ({
    locals
}) => {
    const { client } = locals
    console.log(env.API_URL)
    const res = await getEvents({
        client: client
    })
        let events: EventResponse[] | undefined
    events = res.data?.items ?? []

    return { events: events };
}) satisfies PageServerLoad;