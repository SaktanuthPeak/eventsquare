import { redirect } from "@sveltejs/kit";
import type { RequestHandler } from "./$types";

export const GET: RequestHandler = async ({ cookies }) => {
  // Clear the access_token cookie
  cookies.set("access_token", "", {
    path: "/",
    httpOnly: true,
    sameSite: "strict",
    secure: true,
    maxAge: 0, // Expire immediately
  });

  // Redirect to the login page
  throw redirect(302, "/");
};
