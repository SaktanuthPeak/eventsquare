import { getEventById, getHardTicketsByOrganizerAndEventId } from "$lib/client";
import type { LayoutServerLoad } from "./$types";
import { error } from "@sveltejs/kit";

export const load: LayoutServerLoad = async ({ locals, params }) => {
  const { client } = locals;
  try {
    const eventResponse = await getEventById({
      client: client,
      path: { event_id: params.event },
    });

    return {
      user: locals.user,
      organization_id: params.organization,
      event_id: params.event,
      eventData: eventResponse.data,
    };
  } catch (err) {
    console.error("Error loading event data:", err);
    throw error(404, "Event not found");
  }
};
