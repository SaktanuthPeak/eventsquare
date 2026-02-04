import { getEventById, } from '$lib/client';
import type { PageServerLoad } from './$types';

export const load = (async ({params , locals}) => {
    const { client } = locals;

    const res = await getEventById({
        client: client,
        path:{
            event_id:params.event
        }
    });

    const user = locals.user;
 
    return {eventId: params.event,eventData:res.data,userData:user,};
}) satisfies PageServerLoad;

