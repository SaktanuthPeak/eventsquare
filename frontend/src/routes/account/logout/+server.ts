import { clearTokens } from '$lib/server/auth.js';
import { redirect } from '@sveltejs/kit';

export async function GET(event) {
	clearTokens(event);
	return redirect(303, '/account/login');
}