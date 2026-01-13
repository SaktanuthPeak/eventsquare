import { redirect, type Handle } from "@sveltejs/kit";

export const handleSession:Handle = async ({ event, resolve }) => {
  const accessToken = event.cookies.get('access_token');
  const refreshToken = event.cookies.get('refresh_token');
  const publicPaths = ['/', '/login', '/register','/events'];
  const userPaths = ['/'];

  const path = event.url.pathname;
  const isPublicPath = publicPaths.some(p => path === p || path.startsWith(p + '/'));
  if (!isPublicPath && !accessToken) {
    throw redirect(303, '');
  }
  if (accessToken && event.locals.user) {
    try {
      if (userPaths.some(p => path === p || path.startsWith(p + '/')) &&
           event.locals.user.roles.includes('user')) {
        throw redirect(303, '/');
      }
    } catch (e) {
      event.cookies.delete('session', { path: '/' });
    }
  }

  return await resolve(event);
};