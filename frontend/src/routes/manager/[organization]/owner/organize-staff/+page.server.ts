import { error } from "@sveltejs/kit";
import type { PageServerLoad } from "./$types";
import { getStaffInOrganizer } from "$lib/client";

export const load: PageServerLoad = async ({ locals,params, url }) => {
  try {
    const organizationId = params.organization;
    const page = Number(url.searchParams.get("page") || 1);
    const size = Number(url.searchParams.get("size") || 10);
    const searchQuery = url.searchParams.get("search") || "";
    const { client } = locals;

    if (!organizationId) {
      throw error(404, "Organization not found");
    }

    const staffRes = await getStaffInOrganizer({
      client: client,
      path: { organizer_id: organizationId },
      query: {
        page: page,
        size: size,
        search: searchQuery,
      },
    });

    return {
      organization_id: organizationId,
      staff: staffRes.data.items || [],
      pagination: {
        currentPage: staffRes.data.page || 1,
        totalPages: staffRes.data.pages || 1,
        totalItems: staffRes.data.total || 0,
        itemsPerPage: staffRes.data.size || 10,
      },
    };
  } catch (err) {
    console.error("Error loading staff data:", err);
    throw error(500, "Failed to load staff data");
  }
};
