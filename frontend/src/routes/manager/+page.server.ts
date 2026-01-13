import { getAffliateWith, getById } from "$lib/client";
import type { Actions } from "@sveltejs/kit";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ locals }) => {
  const { client } = locals;
  try {
    const response = await getAffliateWith({
      client : client,
      path: { user_id: locals.user.id },
    });

    return {
      Organization: response.data,
      user: locals.user,
    };
  } catch (error) {
    console.error("Error fetching organizations:", error);
    return {
      Organization: [],
      user: locals.user,
    };
  }
};

