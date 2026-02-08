import { getEvents,getImage, type EventResponse } from '$lib/client';

import type { PageServerLoad } from './$types';
import { env } from '$env/dynamic/private';

export const load: PageServerLoad = async ({ params, url, locals }) => {
    const { client } = locals;
    try {
        const page = Number(url.searchParams.get("page") || 1);
        const size = Number(url.searchParams.get("size") || 50);
        const searchQuery = url.searchParams.get("search") || '';

        let events: EventResponse[] | undefined;

        if (searchQuery) {
            const eventSearchRes = await getEvents({
                query: {
                    name: searchQuery,
                    page,
                    size
                }
            });
            events = eventSearchRes.data?.items ?? [];
        } else {
            const res = await getEvents({client: client});
            events = res.data?.items ?? [];
        }

        const eventsWithImages = [];
        for (const event of events) {
            if (event?.image_id) {
                try {
                    const imageRes = await getImage({
                        client: client,
                        path: { image_id: event?.image_id }
                    });
                    eventsWithImages.push({
                        ...event,
                        image_url: `${env.PUBLIC_CLIENT_API_URL || env.PUBLIC_BASE_API_URL}/v1/images/${imageRes?.data}`
                    });
                } catch (error) {
                    console.log(error);
                }
            } else {
                eventsWithImages.push({
                    ...event,
                    image_url: null
                });
            }
        }

        return { events: eventsWithImages };

    } catch (err) {
        console.error("Error loading events:", err);
        return { events: [] };
    }
};