import type { Handle } from '@sveltejs/kit';
import jwt from 'jsonwebtoken';

import { getMe, refreshToken as refreshTokenRequest } from '$lib/client';
import { logger } from '$lib/logger';
import { constructCookieOptions } from '$lib/shares/cookies';
import { logout } from '$lib/shares/logout';

function isAdminRoute(routeId?: string | null): boolean {
	return Boolean(routeId && routeId.includes('(admin)'));
}

function isAdminPath(pathname: string, routeId?: string | null): boolean {
	return isAdminRoute(routeId) || pathname === '/admin' || pathname.startsWith('/admin/');
}

function hasAdminRole(user: unknown): boolean {
	const roles = (user as { roles?: unknown })?.roles;
	return Array.isArray(roles) && roles.includes('admin');
}

function isTokenExpired(token?: string, bufferSeconds = 300): boolean {
	if (!token) return true;
	try {
		const decoded = jwt.decode(token) as { exp?: number } | null;
		if (!decoded?.exp) return true;
		return Date.now() / 1000 >= decoded.exp - bufferSeconds;
	} catch (err) {
		logger.error({ err }, 'Error decoding token');
		return true;
	}
}

export const authHandler: Handle = async ({ event, resolve }) => {
	const { route, url, cookies, locals } = event;
	const pathname = url.pathname;

	const adminOnly = isAdminPath(pathname, route.id);

	async function populateUserOrClear(enforceAuth: boolean): Promise<void | Response> {
		const accessToken = cookies.get('access_token');
		const refreshToken = cookies.get('refresh_token');
		let effectiveAccessToken = accessToken;

		if (!accessToken && !refreshToken) {
			locals.user = undefined;
			return;
		}

		if (accessToken) {
			locals.client?.setConfig?.({
				headers: { Authorization: `Bearer ${accessToken}` }
			});
		}

		if (isTokenExpired(accessToken)) {
			if (!isTokenExpired(refreshToken)) {
				try {
					const { data } = (await refreshTokenRequest({
						client: locals.client,
						headers: refreshToken ? { Authorization: `Bearer ${refreshToken}` } : undefined
					})) as { data?: any };

					const nextAccessToken: string | undefined = data?.access_token;
					if (nextAccessToken) {
						effectiveAccessToken = nextAccessToken;
						cookies.set(
							'access_token',
							nextAccessToken,
							constructCookieOptions(30 * 60, url)
						);
						locals.client?.setConfig?.({
							headers: { Authorization: `Bearer ${nextAccessToken}` }
						});
					}
				} catch (err) {
					logger.debug({ err }, 'error refreshing token');
					logout(cookies);
					locals.user = undefined;
					return enforceAuth ? redirectToLogin() : undefined;
				}
			} else {
				logout(cookies);
				locals.user = undefined;
				return enforceAuth ? redirectToLogin() : undefined;
			}
		}

		try {
			const meRes = await getMe({
				client: locals.client
			});

			if (!meRes.response.ok) {
				logger.debug({ status: meRes.response.status }, 'Error getting user details');
				logout(cookies);
				locals.user = undefined;
				return enforceAuth ? redirectToLogin() : undefined;
			}

			locals.user = (meRes.data ?? undefined) as any;
		} catch (err) {
			logger.debug({ err }, 'Error getting user details');
			logout(cookies);
			locals.user = undefined;
			return enforceAuth ? redirectToLogin() : undefined;
		}
	}

	async function redirectToLogin(): Promise<Response> {
		logger.debug('Authentication failed, clearing cookies and redirecting to login');
		logout(cookies);
		locals.user = undefined;

		if (pathname === '/account/login') {
			return await resolve(event);
		}

		const redirectUrl = new URL('/account/login', url);
		redirectUrl.searchParams.set('redirect', pathname);
		return Response.redirect(redirectUrl, 302);
	}

	function redirectForbidden(): Response {
		locals.user = undefined;
		return Response.redirect(new URL('/', url), 302);
	}

	// Populate `locals.user` for all routes when tokens exist.
	// - For non-admin routes: best-effort (never redirects)
	// - For admin routes: enforced (redirects to login when invalid)
	const maybeRedirect = await populateUserOrClear(adminOnly);
	if (maybeRedirect) return maybeRedirect;

	// Only enforce role-based access for admin routes.
	if (!adminOnly) {
		return resolve(event);
	}

	if (!hasAdminRole(locals.user)) {
		return redirectForbidden();
	}

	return resolve(event);
};
