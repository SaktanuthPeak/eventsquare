import { getUserTickets } from '$lib/client';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ locals }) => {
    try {
        const { client } = locals;
        const ticketsRes = await getUserTickets({
            client: client,
            path: {user_id: locals?.user?.id}
        });
        const checkedInHistory = ticketsRes?.data?.filter(
            (ticket) => ticket.is_checked_in === true
        ) || [];
        return { checkedInHistory };

    } catch (error) {
        console.error('Error fetching tickets:', error);
        return { checkedInHistory: [] };
    }
};