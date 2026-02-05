import { getUserTicketById } from '$lib/client';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = (async ({locals}) => {
    try {
        const { client } = locals;
        const ticketsRes = await getUserTicketById({
            client: client,
            path: {user_id: locals?.user?.id}
        });

        
        if (ticketsRes?.data) {
            const today = new Date();
            today.setHours(0, 0, 0, 0);
            
            const activeTickets = ticketsRes.data
            
            return { tickets: activeTickets };
        }
        
        return { tickets: [] };
    } catch (error) {
        console.error('Error fetching tickets:', error);
        return { tickets: [] };
    }
});