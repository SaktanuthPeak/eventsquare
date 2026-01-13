import { error } from "@sveltejs/kit";
import type { PageServerLoad } from "./$types";
import {
  getEventRelatedWithOrganizer,
  getOrganizerCompleteInfo,
} from "$lib/client";

export const load: PageServerLoad = async ({ params, locals }) => {
  try {
    const { client } = locals;
    const user = locals.user;

    if (!user) {
      throw error(401, "Please log in to access this page");
    }

    const organizationId = params.organization;

    if (!organizationId) {
      throw error(404, "Organization not found");
    }

    const organizationResponse = await getOrganizerCompleteInfo({
      client: client,
      path: { organizer_id: organizationId },
    });

    const event = await getEventRelatedWithOrganizer({
      client: client,
      path: { organizer_id: organizationId },
    });

    return {
      user,
      organization_id: organizationId,
      organization: organizationResponse.data,
      events: event.data,
    };
  } catch (error) {
    console.error("Failed to load organization data:", error);
    return {
      user: locals.user,
      organization_id: params.organization,
      events: [],
    };
  }
};
