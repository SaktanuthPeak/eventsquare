import { getMe, refreshToken as verifyRefreshToken } from '$lib/client';
import { logger } from '$lib/logger';
import { constructCookieOptions } from '$lib/shares/cookies';
import { logout } from '$lib/shares/logout';
import type { Handle } from '@sveltejs/kit';
import jwt from 'jsonwebtoken';

interface RefreshTokenResponse {
	access_token?: string;
}

function isAdminRoute(routeId?: string | null): boolean {
	return Boolean(routeId && routeId.includes('(admin)'));
}

function hasAdminRole(user: unknown): boolean {
	const roles = (user as { roles?: unknown })?.roles;
	return Array.isArray(roles) && roles.includes('admin');
}


function isProtectedRoute(path: string | null): boolean {
	if (!path) return false;

	return (
		path.startsWith('/menu') ||
		path.includes('/checkout') ||
		path.includes('/check-in')
	);
}

export const authHandler: Handle = async ({ event, resolve }) => {
	const { route, url, cookies, locals } = event;
	const { client } = locals;
	function handleAuthFailure() {
		logger.debug('Authentication failed, clearing cookies and redirecting to login');
		logout(cookies);
		locals.user = undefined;

		if (route.id?.includes('api')) {
			return new Response(JSON.stringify({ error: 'Unauthorized' }), {
				status: 401,
				headers: { 'Content-Type': 'application/json' },
			});
		} else {
			if (url.pathname === '/account/login') {
				return resolve(event);
			}
			const redirectUrl = new URL('/account/login', url);
			redirectUrl.searchParams.set('redirect', url.pathname);
			return Response.redirect(redirectUrl, 302);
		}
	}

	function handleAdminForbidden() {
		if (route.id?.includes('api')) {
			return new Response(JSON.stringify({ error: 'Forbidden' }), {
				status: 403,
				headers: { 'Content-Type': 'application/json' },
			});
		}
		return Response.redirect(new URL('/', url), 302);
	}

	const isAdminPath = isAdminRoute(route.id) || url.pathname.startsWith('/admin');
	const isProtected = isProtectedRoute(url.pathname) || isAdminPath;

	const accessToken = cookies.get('access_token');
	const refreshToken = cookies.get('refresh_token');

	if (!accessToken && !refreshToken) {
		locals.user = undefined;
		return isProtected ? handleAuthFailure() : resolve(event);
	}

	const isExpired = isTokenExpired(accessToken);
	if (accessToken) {
		client.setConfig({
			headers: {
				Authorization: `Bearer ${accessToken}`,
			}
		});
	}
	logger.debug(`Access token expired: ${isTokenExpired(accessToken)}`);
	logger.debug(`Refresh token expired: ${isTokenExpired(refreshToken)}`);
	if (isExpired) {
		logger.debug('Access token is expired, checking refresh token');
		if (!isTokenExpired(refreshToken)) {
			try {
				const { data } = await verifyRefreshToken({
					client: client,
					headers: {
						Authorization: `Bearer ${refreshToken}`,
					}
				}) as { data: RefreshTokenResponse };
				if (data?.access_token) {
					logger.debug('Refresh token is valid, updating access token');
					cookies.set('access_token', data.access_token, constructCookieOptions(30 * 60)); // 1 day
					client.setConfig({
						headers: {
							Authorization: `Bearer ${data.access_token}`,
						}
					});
				}
			} catch (err) {
				logger.debug({ err }, 'error refreshing token');
				logout(cookies);
				locals.user = undefined;
				return isProtected ? handleAuthFailure() : resolve(event);
			}
		} else {
			logger.debug('Access token & Refresh Token expired, delete cookies and redirecting to login');
			logout(cookies);
			locals.user = undefined;
			return isProtected ? handleAuthFailure() : resolve(event);
		}
	}

	try {
		const { data } = await getMe({
			client: client,
		});
		locals.user = data;
	} catch (err) {
		logger.debug({ err }, 'Error getting user details');
		logout(cookies);
		locals.user = undefined;
		return isProtected ? handleAuthFailure() : resolve(event);
	}

	if (isAdminPath && !hasAdminRole(locals.user)) {
		return handleAdminForbidden();
	}

	return resolve(event);
}

function isTokenExpired(token?: string, bufferTime = 300): boolean {
	if (!token) return true;
	try {
		const decoded = jwt.decode(token) as { exp?: number } | null;
		if (!decoded || !decoded.exp) return true;
		return Date.now() / 1000 >= decoded.exp - bufferTime;
	} catch (error) {
		logger.error({ err: error }, 'Error decoding token');
		return true;
	}
}