import { error } from "@sveltejs/kit";
import type { PageServerLoad, Actions } from "./$types";
import { getPublicTicketVerificationLogs } from "$lib/client";

export const load: PageServerLoad = async ({ locals,params, url }) => {
  const { client } = locals;
  try {
    const page = Number(url.searchParams.get("page") || 1);
    const size = Number(10);
    const searchQuery = url.searchParams.get("search") || "";
    const dateParam = url.searchParams.get("date") || "";
    const date = dateParam
      ? new Date(dateParam).toISOString().split("T")[0] // Returns YYYY-MM-DD
      : "";

    const checkInUserRes =
      (await getPublicTicketVerificationLogs({
        client: client,
        path: { event_id: params.event },
        query: { page: page, size: size, owner_name: searchQuery, date: date },
      })) || [];

    const total = checkInUserRes?.data?.total || 0;
    const totalPages = Math.max(
      1,
      Math.ceil(checkInUserRes?.data?.total / size)
    );

    return {
      organization_id: params.organization,
      event_id: params.event,
      eventData: {
        checkInUser: checkInUserRes.data.items,
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
