import type { Cookies } from '@sveltejs/kit';
import { constructCookieOptions } from './cookies';

export function logout(cookies: Cookies) {
	// Delete cookies with comprehensive options to ensure complete removal
	cookies.delete('access_token', {
		path: '/'
	});
	cookies.delete('refresh_token', {
		path: '/'
	});

	// Also try to delete with different path variations to be thorough
	cookies.delete('access_token', { path: '' });
	cookies.delete('refresh_token', { path: '' });

	// Set empty values as additional measure
	cookies.set('access_token', '', constructCookieOptions(0));
	cookies.set('refresh_token', '', constructCookieOptions(0));
}