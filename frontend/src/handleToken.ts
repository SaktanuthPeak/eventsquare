import { getMe } from "$lib/client";
import type { Handle } from "@sveltejs/kit";

export const handleToken: Handle = async ({ event, resolve }) => {
  const accessToken = event.cookies.get("access_token");
  const { client } = event.locals;
  if (event.locals.user) {
    return await resolve(event);
  }


  if (accessToken) {
    try {
      const res = await getMe({
        client:client,
      });

      if (res.response.status === 200 && res.data) {
        const userData = res.data;
        event.locals.user = {
          id: userData.id,
          username: userData.username,
          first_name: userData.first_name,
          last_name: userData.last_name,
          roles: userData.roles,
        };
      } else {
        console.log("Failed to fetch user data");
      }
    } catch (error) {
      console.error("Error fetching user data:", error);
    }
  }

  return await resolve(event);
};
