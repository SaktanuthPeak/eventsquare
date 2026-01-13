import { getOrdersByOrganizer } from "$lib/client";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({locals,params,url}) => {  
    const { client } = locals;
    const res = await getOrdersByOrganizer({
        client: client,
        path: {
            organizer_id: params.organization,
            event_id: params.event,
        },
    })

    const page = Number(url.searchParams.get("page") || 1);
    const size = Number(url.searchParams.get("size") || 10);
    const searchQuery = url.searchParams.get("search") || "";

    const allOrders = res.data || [];

    const filteredOrders = searchQuery ? allOrders.filter((order) =>
        order.order_number?.toLowerCase().includes(searchQuery.toLowerCase())
    ) : allOrders;

    const total = filteredOrders.length;
    const totalPages = Math.max(1, Math.ceil(total / size));
    const start = (page - 1) * size;
    const end = Math.min(start + size, total);
    const paginatedOrders = filteredOrders.slice(start, end);

    return {
        orders: paginatedOrders,
        
        pagination: {
            currentPage: page,
            totalPages: totalPages,
            totalItems: total,
            itemsPerPage: size,
      },
    }
};

