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
	const baseOptions = constructCookieOptions(0);
	cookies.set('access_token', '', baseOptions);
	cookies.set('refresh_token', '', baseOptions);

	// Also clear using both secure modes, in case cookies were previously set incorrectly
	cookies.set('access_token', '', { ...baseOptions, secure: true });
	cookies.set('refresh_token', '', { ...baseOptions, secure: true });
	cookies.set('access_token', '', { ...baseOptions, secure: false });
	cookies.set('refresh_token', '', { ...baseOptions, secure: false });
}