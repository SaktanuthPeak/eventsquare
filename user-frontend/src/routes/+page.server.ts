import { getAllEvents, type EventResponse } from '$lib/client';
import { fail } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import { env } from '$env/dynamic/private';
export const load = (async ({
    locals
}) => {
    // todo change to fetch all events after this api test for check in function
    const { client } = locals
    console.log(env.API_URL)
    const res = await getAllEvents({
        client: client
    })
    let events: EventResponse[] | undefined
    events = res.data?.items ?? []

    const eventsWithImages = [];
    for (const event of events) {

        if (event.image?.file_id) {
            try {

                eventsWithImages.push({
                    ...event,
                    image_url: `${env.API_URL}/v1/events/image/${event.image.file_id}`
                })

            } catch (error) {
                console.log(error)
            }
        } else {
            eventsWithImages.push({
                ...event,
                image_url: null
            })
        }
    }

    return { events: eventsWithImages.filter((event) => event.event_status === 'active') };
}) satisfies PageServerLoad;