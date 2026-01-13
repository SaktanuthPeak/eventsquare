import { getAllEvents, type EventResponse } from '$lib/client';
import { get } from 'svelte/store';
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
            const eventSearchRes = await getAllEvents({
                client: client,
                query: {
                    search_query: searchQuery,
                    page,
                    size
                }
            });
            events = eventSearchRes.data?.items ?? [];
        } else {
            const res = await getAllEvents({client: client});
            events = res.data?.items ?? [];
        }

        const eventsWithImages = [];
        for (const event of events) {
            if (event.image?.file_id) {
                try {
                    eventsWithImages.push({
                        ...event,
                        image_url: `${env.API_URL}/v1/events/image/${event.image.file_id}`
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

        return { events: eventsWithImages.filter((event) => event.event_status === 'active') };

    } catch (err) {
        console.error("Error loading events:", err);
        return { events: [] };
    }
};