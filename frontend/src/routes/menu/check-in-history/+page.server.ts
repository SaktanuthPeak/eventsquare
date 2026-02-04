import { getTicketsByUserId } from '$lib/client';
import type { PageServerLoad } from './$types';

export const load : PageServerLoad = (async ({locals}) => {
    const { client } = locals;
    const checkInRes = await getTicketsByUserId({
        client: client,
        path:{user_id: locals.user?.id }
        });
    return {checkedInHistory: checkInRes?.data?.filter((ticket) => ticket.ticket_type_name === null)};
});