import { env } from '$env/dynamic/public';
import { getImage } from '$lib/client';
import { getEventById } from '$lib/client';
import type { PageServerLoad } from './$types';

export const load = (async ({params , locals}) => {
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
                                            path: { image_id: res?.data?.image_id }
                                        });
                    image_url = `${env.PUBLIC_API_URL}/v1/images/${imageRes?.data}`
                } catch (error) {
                    console.log(error);
                }
            } else {
                    image_url = null
            }

    return {
        eventId: params.event,
        eventData: res.data,
        userData: locals.user,
        image: image_url,
        orgData: (res.data as any)?.organizer
    };
}) satisfies PageServerLoad;

