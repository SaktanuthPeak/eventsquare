import { getAffliateWith, getOrganizerCompleteInfo } from "$lib/client";
import type { LayoutServerLoad } from "./$types";

export const load: LayoutServerLoad = async ({ locals, params }) => {
  
  const { client } = locals;
  const orgUserDataRes = await getAffliateWith({
    client: client,
    path: {
      user_id: locals.user.id,
    },
  });

  if (params.organization) {
    const orgDataRes = await getOrganizerCompleteInfo({
      client: client,
      path: {
        organizer_id: params.organization,
      },
    });
    return {
      orgUserData: orgUserDataRes.data || [],
      orgData: orgDataRes?.data || [],
      user: locals.user,
      organization_id: params.organization,
      event_id: params.event,
    };
  } else {
    return {
      orgUserData: orgUserDataRes.data || [],
      orgData: [],
      user: locals.user,
      organization_id: params.organization,
      event_id: params.event,
    };
  }
};
