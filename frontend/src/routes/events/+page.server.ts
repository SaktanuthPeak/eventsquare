import {  getEvents, type EventResponse } from '$lib/client';
import type { PageServerLoad } from './$types';

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

    } catch (err) {
        console.error("Error loading events:", err);
        return { events: [] };
    }
};