import { getOrdersByUserId } from '$lib/client';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = (async ({locals}) => {
    const { client } = locals;
    const orderRes = await getOrdersByUserId({
        client: client,
        path:{ user_id: locals?.user?.id}
    })
    return {orders: orderRes?.data};
});