import { getEventById, getUserTicketById } from '$lib/client';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = (async ({locals}) => {
    const { client } = locals;
    try {
        const ticketsRes = await getUserTTicketById({
            client: client,
            path: {user_id: locals?.user?.id}
        });

        
        if (ticketsRes?.data) {
            const today = new Date();
            today.setHours(0, 0, 0, 0);
            
            const activeTickets = ticketsRes.data.filter(ticket => {
                if (ticket.ticket_status === 'used') {
                    return false;
                }
                
                if (ticket.allowed_dates) {
                    if (ticket.allowed_dates.date_range) {
                        const endDate = new Date(ticket.allowed_dates.date_range.end_date);
                        return endDate <= today; 
                    } else if (ticket.allowed_dates.single_date) {
                        const ticketDate = new Date(ticket.allowed_dates.single_date);
                        return ticketDate <= today;
                    }
                }
                
                return true;
            });
            
            return { tickets: activeTickets };
        }
        
        return { tickets: [] };
    } catch (error) {
        console.error('Error fetching tickets:', error);
        return { tickets: [] };
    }
});