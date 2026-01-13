import { redirect, type Handle } from "@sveltejs/kit";
import { getOrganizerCompleteInfo } from "$lib/client";

export const handleSession: Handle = async ({ event, resolve }) => {
  const accessToken = event.cookies.get("access_token");
  const publicPaths = ["/", "/login", "/register"];
  const adminPaths = ["/admin"];
  const userPaths = ["/manager"];

  const path = event.url.pathname;

  // Basic auth check
  const isPublicPath = publicPaths.some(
    (p) => path === p || path.startsWith(p + "/")
  );
  if (!isPublicPath && !accessToken) {
    throw redirect(303, "/");
  }

  // Make sure user data is available
  if (!event.locals.user && accessToken) {
    event.cookies.delete("access_token", { path: "/" });
    throw redirect(303, "/");
  }

  // Check for owner route access
  if (path.includes("/owner/") && event.locals.user) {
    const ownerPathMatch = path.match(/\/manager\/([^\/]+)\/owner\//);
    const { client } = event.locals;
    if (ownerPathMatch && ownerPathMatch[1]) {
      const organizationId = ownerPathMatch[1];

      try {
        // Get organization info
        const orgInfo = await getOrganizerCompleteInfo({
          client: client,
          path: { organizer_id: organizationId },
        });

        // Check if user is owner or co-owner
        const isOwner =
          orgInfo.data?.organizer.manager_id === event.locals.user.id;
        const isCoOwner = orgInfo.data?.organizer.co_manager_id?.includes(
          event.locals.user.id
        );

        // Redirect to staff route if not owner or co-owner
        if (!isOwner && !isCoOwner) {
          // Replace /owner/ with /staff/ in the current path
          const staffPath = path.replace("/owner/", "/staff/");
          throw redirect(303, staffPath);
        }
      } catch (error) {
        // This is a genuine error
        console.error("Organization access error:", error);
        throw redirect(303, "/manager");
      }
    }
  }

  if (accessToken && event.locals.user) {
    if (
      adminPaths.some((p) => path === p || path.startsWith(p + "/")) &&
      !event.locals.user.roles.includes("admin")
    ) {
      throw redirect(303, "/");
    }
  }

  return await resolve(event);
};
