import { createTicket } from '$lib/client';
import type { PageServerLoad } from './$types';

export const load = (async () => {
    return {};
}) satisfies PageServerLoad;

export const actions = {
    default: async ({ request }) => {

    // try{
    //     //todo add logic for create ticket
    //     const res = await createTicket({
    //         body: {
    //             event_id: '', // Add your event ID
    //             owner_name: '', // Add owner name
    //             co_owner_name: '', // Add co-owner name
    //             ticket_type_id: '',
    //             ticket_format: '',
    //             audience_per_ticket: 0
    //         }
    //     })
    // }catch (error) {
    //     console.error('Error:', error);
    //     return {
    //         error: 'Failed to process QR code'
    //     };
    // }
}}