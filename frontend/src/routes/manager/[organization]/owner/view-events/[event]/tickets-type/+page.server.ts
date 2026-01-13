import { error } from "@sveltejs/kit";
import { getEventById, deleteTicketType } from "$lib/client";
import type { PageServerLoad, Actions } from "./$types";

export const load: PageServerLoad = async ({ locals,params, url }) => {
  const {client} = locals
  try {
    const page = Number(url.searchParams.get("page") || 1);
    const size = Number(url.searchParams.get("size") || 10);
    const searchQuery = url.searchParams.get("search") || "";

    const eventResponse = await getEventById({
      client: client,
      path: { event_id: params.event },
    });

    const allTicketTypes = eventResponse.data?.ticket_types || [];
    const filteredTickets = searchQuery
      ? allTicketTypes.filter((ticket) =>
          ticket.name?.toLowerCase().includes(searchQuery.toLowerCase())
        )
      : allTicketTypes;

    const total = filteredTickets.length;
    const totalPages = Math.max(1, Math.ceil(total / size));
    const start = (page - 1) * size;
    const end = Math.min(start + size, total);
    const paginatedTickets = filteredTickets.slice(start, end);

    return {
      organization_id: params.organization,
      event_id: params.event,
      eventData: {
        ticket_types: paginatedTickets,
        total_ticket_types: total,
      },
      pagination: {
        currentPage: page,
        totalPages: totalPages,
        totalItems: total,
        itemsPerPage: size,
      },
    };
  } catch (err) {
    console.error("Error loading ticket types:", err);
    throw error(500, "Failed to load ticket types");
  }
};

export const actions: Actions = {
  // server action สำหรับลบ ticket
  deleteTicket: async ({ locals,request }) => {
    const formData = await request.formData();
    const ticketTypeId = formData.get("ticket_type_id") as string;
    const { client } = locals;
    if (!ticketTypeId) {
      return { success: false, error: "No ticket ID provided" };
    }

    try {
      const response = await deleteTicketType({
        client: client,
        path: { ticket_type_id: ticketTypeId },
      });

      if (response.status === 200) {
        return {
          success: true,
          message: "Ticket type deleted successfully",
        };
      } else {
        return {
          success: false,
          error: response.error?.message || "Failed to delete ticket type",
        };
      }
    } catch (error) {
      console.error("Error deleting ticket type:", error);
      return {
        success: false,
        error: "An error occurred while deleting the ticket type",
      };
    }
  },
};
