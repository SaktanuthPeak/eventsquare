import { superValidate } from 'sveltekit-superforms';
import type { PageServerLoad } from './$types';
import  { checkInSchema }  from './schema';
import { zod } from 'sveltekit-superforms/adapters';
import { getEventById, getUserTicketById } from '$lib/client';
import { fail, redirect } from '@sveltejs/kit';

export const load = (async (event) => {
    const { client } = event.locals;
    const form = await superValidate(zod(checkInSchema));
    const res = await getEventById({
        client: client,
        path:{
            event_id: event.params.event
        }
    })

    if(res.data?.event_type !== "public"){
        throw redirect(302, `/events/${event.params.event}`);
    }
    
    // Fetch ticket details
    let ticketData = null;
    try {
        const ticketRes = await getUserTicketById({
            client: client,
            path: {
                user_ticket_id: event.params.ticket
            }
        });
        ticketData = ticketRes.data;
    } catch (err) {
        console.error('Error fetching ticket:', err);
    }
    
    return {
        eventId: event.params.event,
        ticket: event.params.ticket,
        ticketData,
        form,
        userData: event.locals.user
    };
}) satisfies PageServerLoad;

export const actions = {
    default: async (event) => {
        const { client } = event.locals;
        const form = await superValidate(event, zod(checkInSchema));
        if (!form.valid) {
            return fail(400, { form });
        }
        
        if (!event.locals.user) {
            return fail(401, { form, error: 'Unauthorized' });
        }

        try {
            const res = await publicCheckIn({
                client: client,
                headers:{
                    Authorization: `Bearer ${event.cookies.get("access_token")}`
                },
                path:{
                    event_id: event.params.event
                }
            });

            if(!res.response.ok){
                return fail(res.response.status, {
                    form,
                    error: `Failed to check-in: ${res.error?.errors?.[0] || 'Unknown error'}`
                });
            }

            return {
                form,
                returnData: res.data,
                success: true
            };
        } catch (error) {
            console.error("Check-in error:", error);
            return fail(500, {
                form,
                error: 'Failed to create ticket'
            });
        }
    }
};