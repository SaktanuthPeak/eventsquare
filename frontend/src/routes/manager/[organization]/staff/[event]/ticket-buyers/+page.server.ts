import { getTicketsByEventId } from "$lib/client";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ locals,params, url }) => {
  const {client} = locals
  try {
    const page = Number(url.searchParams.get("page") || 1);
    const size = Number(url.searchParams.get("size") || 10);
    const searchQuery = url.searchParams.get("search") || "";

    const ticketRes = await getTicketsByEventId({
      client: client,
      path: { event_id: params.event, page: page, size: size },
    });

    // Check if the response is valid
    const allTickets = ticketRes.data || [];
    // Filter tickets based on the search query
    const filleredTicket = searchQuery
      ? allTickets.filter((ticket) =>
          ticket.ticket_type_name
            ?.toLowerCase()
            .includes(searchQuery.toLowerCase())
        )
      : allTickets;

    return {
      ticketData: filleredTicket,
      total_ticket_types: allTickets.length,
      organization_id: params.organization,
      event_id: params.event,
    };
  } catch (err) {
    console.error("Error loading ticket types:", err);
    throw error(500, "Failed to load ticket types");
  }
};
