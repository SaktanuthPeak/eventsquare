import { getMe, refreshToken as verifyRefreshToken } from '$lib/client';
import { logger } from '$lib/logger';
import { constructCookieOptions } from '$lib/shares/cookies';
import { logout } from '$lib/shares/logout';
import type { Handle } from '@sveltejs/kit';
import jwt from 'jsonwebtoken';

// --- HELPER FUNCTIONS (TOP LEVEL) ---

function isProtectedRoute(path: string | null): boolean {
	if (!path) return false;

	return path.split('/').includes('(auth)');
}

export const authHandler: Handle = async ({ event, resolve }) => {
	const { route, url, cookies, locals } = event;
	const { client } = locals;

	// Helper function to handle authentication failures
	function handleAuthFailure() {
		logger.debug('Authentication failed, clearing cookies and redirecting to login');
		logout(cookies);
		locals.user = undefined;

		if (route.id?.includes('api')) {
			// If it's an API route, return a 401 Unauthorized response
			return new Response(JSON.stringify({ error: 'Unauthorized' }), {
				status: 401,
				headers: { 'Content-Type': 'application/json' },
			});
		} else {
			// Avoid redirect loops - don't redirect if already on login page
			if (url.pathname === '/account/login') {
				return resolve(event);
			}
			const redirectUrl = new URL('/account/login', url);
			redirectUrl.searchParams.set('redirect', url.pathname);
			return Response.redirect(redirectUrl, 302);
		}
	}

	const isProtected = isProtectedRoute(route.id);

	// Handle public routes (login, register, etc.)
	if (!isProtected) {
		return resolve(event);
	}

	const accessToken = cookies.get('access_token');
	const refreshToken = cookies.get('refresh_token');
	const isExpired = isTokenExpired(accessToken);
	client.setConfig({
		headers: {
			Authorization: `Bearer ${accessToken}`,
		}
	})
	logger.debug(`Access token expired: ${isTokenExpired(accessToken)}`);
	logger.debug(`Refresh token expired: ${isTokenExpired(refreshToken)}`);
	if (isExpired) {
		logger.debug('Access token is expired, checking refresh token');
		// ตรงนี้ควรจะลอง get refresh token และขอ access token ใหม่
		if (!isTokenExpired(refreshToken)) {
			try {
				const { data } = await verifyRefreshToken({
					client: client,
					headers: {
						Authorization: `Bearer ${refreshToken}`,
					}
				});
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
				logger.debug('error refreshing token:', err);
				return handleAuthFailure();
			}
		} else {
			logger.debug('Access token & Refresh Token expired, delete cookies and redirecting to login');
			return handleAuthFailure();
		}
	}

	try {
		const { data } = await getMe({
			client: client,
		});
		locals.user = data;
	} catch (err) {
		logger.debug('Error getting user details:', err);
		return handleAuthFailure();
	}

	return resolve(event);
}

// This function checks if the JWT token is expired based on its payload and a buffer time
// bufferTime is the time in seconds before expiration to consider the token as expired
function isTokenExpired(token?: string, bufferTime = 300): boolean {
	if (!token) return true;
	try {
		const decoded = jwt.decode(token) as { exp?: number } | null;
		if (!decoded || !decoded.exp) return true;
		return Date.now() / 1000 >= decoded.exp - bufferTime;
	} catch (error) {
		logger.error('Error decoding token:', error);
		return true;
	}
}