import { redirect } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { constructCookieOptions } from '$lib/shares/cookies';

export const GET: RequestHandler = async ({ cookies }) => {
	cookies.delete('access_token', constructCookieOptions(0));
	cookies.delete('refresh_token', constructCookieOptions(0));
	// Redirect to the login page
	throw redirect(302, '/account/login');
};