import { getOrdersByUserId, getTicketsByUserId } from '$lib/client';
import type { PageServerLoad } from './$types';

export const load = (async ({locals}) => {
    const { client } = locals;
    const ticketRes = await getTicketsByUserId({
        client: client,
        path:{user_id:locals.user.id}});
    const orderRes = await getOrdersByUserId({
        client: client,
        path:{user_id:locals.user.id}});

    const totalSpent = orderRes.data ? orderRes.data.filter((status:any)=> status.order_status === 'completed').reduce((acc, order:any) => acc + order.total_amount, 0) : 0;

    return {user: locals.user,totalSpent: totalSpent};
}) satisfies PageServerLoad;