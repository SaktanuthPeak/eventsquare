import { error, redirect } from '@sveltejs/kit';
import type { Handle, RequestEvent } from '@sveltejs/kit';
import { ACCESS_TOKEN_COOKIE_NAME, REFRESH_TOKEN_COOKIE_NAME } from './global';
import { apiFetch } from './api';
import type { IBackOfficeUser } from '$lib/models/back-office-users';
import type { AuthTokenResponse } from '$lib/models/auth';

export function isProtectedRoute(event: RequestEvent) {
	return event.route.id && event.route.id.includes('(protected)');
}

export function isProtectedApi(event: RequestEvent) {
	return event.route.id && event.route.id.includes('/api/(protected)');
}

export const handleUserAuth: Handle = async ({ event, resolve }) => {
	const { cookies, locals, url } = event;
	const pathname = url.pathname;

	let response;
	let currentUser;
	if (cookies.get(REFRESH_TOKEN_COOKIE_NAME)) {
		if (!cookies.get(ACCESS_TOKEN_COOKIE_NAME)) {
			await refreshAccessToken(event);
		}
		try {
			response = await getBackOfficeUserProfile(event);
			if (response.data) {
				locals.back_office_user = response.data;
				currentUser = response.data;
			}
		} catch (err) {
			console.error('error hook get user profile', err);
		}
		locals.token = cookies.get(ACCESS_TOKEN_COOKIE_NAME);
	}

	const redirectUri = encodeURIComponent(pathname);
	if (response?.status === 401 || !currentUser) {
		clearTokens(event);
		return redirect(303, `/account/login?redirect_from=${redirectUri}`);
	} else if (!currentUser.is_password_setup) {
		return redirect(303, `/account/setup-password?redirect_from=${redirectUri}`);
	}

	try {
		return await resolve(event, {
			filterSerializedResponseHeaders: (key) => {
				return key.toLowerCase() === 'content-type';
			}
		});
	} catch (err) {
		console.error('error hooks resolve =>', err);
		return error(500, 'Internal server error');
	}
};

export const getBackOfficeUserProfile = async (event: RequestEvent) => {
	const result = await apiFetch<IBackOfficeUser>(event, '/api/v1/back-office/auth/me');
	return result;
};

export function clearTokens(event: RequestEvent) {
	const { cookies } = event;
	cookies.delete(ACCESS_TOKEN_COOKIE_NAME, constructCookieOptions(0));
	cookies.delete(REFRESH_TOKEN_COOKIE_NAME, constructCookieOptions(0));
	event.locals.back_office_user = undefined;
	event.locals.token = undefined;
}

export function saveToken(
	event: RequestEvent,
	accessToken: string,
	accessTokenExpires: string,
	refreshToken: string,
	refreshTokenExpires: string
) {
	const { cookies } = event;
	const now: Date = new Date();
	const access_token_expires: Date = new Date(accessTokenExpires);
	const access_token_max_age: number =
		Math.floor((access_token_expires.getTime() - now.getTime()) / 1000) - 60;
	// set access token expires 60 second early.

	const refresh_token_expires = new Date(refreshTokenExpires);
	const refresh_token_max_age: number =
		Math.floor((refresh_token_expires.getTime() - now.getTime()) / 1000) - 60;
	// set refresh token expires 60 second early.

	cookies.set(ACCESS_TOKEN_COOKIE_NAME, accessToken, constructCookieOptions(access_token_max_age));
	cookies.set(
		REFRESH_TOKEN_COOKIE_NAME,
		refreshToken,
		constructCookieOptions(refresh_token_max_age)
	);
}

export async function refreshAccessToken(event: RequestEvent) {
	const { cookies } = event;
	if (cookies.get(REFRESH_TOKEN_COOKIE_NAME)) {
		const response = await apiFetch<AuthTokenResponse>(
			event,
			'/api/v1/back-office/auth/refresh-token',
			{
				method: 'POST',
				body: JSON.stringify({
					grant_type: 'refresh_token',
					refresh_token: event.cookies.get(REFRESH_TOKEN_COOKIE_NAME)
				})
			}
		);

		const data = response.data;
		if (!data || response.status !== 200) {
			clearTokens(event);
			return false;
		}

		saveToken(
			event,
			data.access_token,
			data.access_token_expires,
			data.refresh_token,
			data.refresh_token_expires
		);
	}
}

export const constructCookieOptions: {
	(expires: number): {
		path: string;
		httpOnly: boolean;
		sameSite: boolean | 'lax' | 'strict' | 'none';
		secure: boolean;
		maxAge: number;
	};
} = (expires: number) => {
	return {
		// send cookie for every page
		path: '/',

		// server side only cookie so you can't use `document.cookie`
		httpOnly: true,

		// only requests from same site can send cookies
		sameSite: 'strict',

		// only sent over HTTPS in production
		secure: process.env.NODE_ENV === 'production',

		// set cookie to expire after a given time
		maxAge: expires
	};
};