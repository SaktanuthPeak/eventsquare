import { env } from '$env/dynamic/public';
import { getImage } from '$lib/client';
import { getEventById } from '$lib/client';
import type { PageServerLoad } from './$types';

export const load = (async ({params , locals}) => {
    try {
        const res = await getEventById({
            client: locals.client,
            path: {
                event_id: params.event
            }
        });

        let image_url: string | null = null;
        if (res?.data?.image_id) {
            try {
                const imageRes = await getImage({
                    client: locals.client,
                    path: { image_id: res.data.image_id }
                });
                image_url = `${env.PUBLIC_CLIENT_API_URL || env.PUBLIC_BASE_API_URL}/v1/images/${imageRes?.data}`;
            } catch (error) {
                console.error('Error loading event image:', error);
            }
        }

        return {
            eventId: params.event,
            eventData: res.data,
            userData: locals.user,
            image: image_url,
            orgData: (res.data as any)?.organizer
        };
    } catch (err) {
        console.error('Error loading event:', err);
        return {
            eventId: params.event,
            eventData: null,
            userData: locals.user,
            image: null,
            orgData: null,
            apiError: 'Backend unavailable'
        };
    }
}) satisfies PageServerLoad;

