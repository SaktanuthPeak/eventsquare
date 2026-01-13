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
  const orgDataRes = await getOrganizerCompleteInfo({
    client: client,
    path: {
      organizer_id: params.organization,
    },
  });

  return {
    orgUserData: orgUserDataRes.data,
    orgData: orgDataRes.data,
    organization_id: params.organization,
    event_id: params.event,
  };
};
