import { getUserTickets } from '$lib/client';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ locals }) => {
    try {
        const { client } = locals;
        const ticketsRes = await getUserTickets({
            client: client,
            path: {user_id: locals?.user?.id}
        });
        // console.log("User tickets response:", ticketsRes);
        const checkedInHistory = ticketsRes?.data?.filter(
            (ticket) => ticket.is_checked_in === true
        ) || [];

        console.log("Checked-in history:", checkedInHistory);
        return { checkedInHistory };

    } catch (error) {
        console.error('Error fetching tickets:', error);
        return { checkedInHistory: [] };
    }
};