import { superValidate } from 'sveltekit-superforms';
import type { PageServerLoad, Actions } from './$types';
import  { checkInSchema }  from './schema';
import { zod } from 'sveltekit-superforms/adapters';
import { getEventById, getUserTicketById } from '$lib/client';
import { fail, redirect } from '@sveltejs/kit';
import { env } from '$env/dynamic/public';

export const load = (async (event) => {
    const { client } = event.locals;
    const form = await superValidate(zod(checkInSchema));
    const res = await getEventById({
        client: client,
        path:{
            event_id: event.params.event
        }
    })
    
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

export const actions: Actions = {
    default: async (event) => {
        const form = await superValidate(event, zod(checkInSchema));
        
        if (!form.valid) {
            return fail(400, { form });
        }
        
        if (!event.locals.user) {
            return fail(401, { form, error: 'Unauthorized' });
        }

        try {
            const baseUrl = env.PUBLIC_BASE_API_URL || 'http://localhost:9000';
            const token = event.cookies.get("access_token");
            const response = await fetch(`${baseUrl}/v1/tickets/check-in/${event.params.ticket}`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });

            if (!response.ok) {
                const errorData = await response.json() as { detail?: string };
                return fail(response.status, {
                    form,
                    error: errorData.detail || 'Failed to check-in'
                });
            }

            const checkInResult = await response.json();

            return {
                form,
                returnData: checkInResult,
                success: true
            };
        } catch (error) {
            console.error("Check-in error:", error);
            return fail(500, {
                form,
                error: 'Failed to check-in: ' + String(error)
            });
        }
    }
} satisfies Actions;