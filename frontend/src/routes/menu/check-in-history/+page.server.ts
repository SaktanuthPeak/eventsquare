import { getUserTickets } from '$lib/client';
import type { PageServerLoad } from './$types';

export const load : PageServerLoad = (async ({locals}) => {
    const checkInRes = await getUserTickets({
        path:{user_id: locals.user?.id }
        });
    return {checkedInHistory: checkInRes?.data};
});