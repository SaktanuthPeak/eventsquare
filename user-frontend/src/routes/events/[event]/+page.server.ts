import { getEventById, getOrganizerCompleteInfo } from '$lib/client';
import { superValidate } from 'sveltekit-superforms';
import type { PageServerLoad } from './$types';
import { selectTicketSchema } from './schema';
import { zod } from 'sveltekit-superforms/adapters';

export const load = (async ({params , locals}) => {
    const { client } = locals;

    const res = await getEventById({
        client: client,
        path:{
            event_id:params.event
        }
    });

    const orgRes = await getOrganizerCompleteInfo({
        client: client,
        path:{
            organizer_id:res.data?.organizer_id
        }
    })

    const user = locals.user;
 
    return {eventId: params.event,eventData:res.data,userData:user,orgData:orgRes.data};
}) satisfies PageServerLoad;

