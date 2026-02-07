import { getEvents, type EventResponse } from '$lib/client';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ locals }) => {
	try {
		const res = await getEvents({ client: locals.client });
		const events = (res.data?.items ?? []) as EventResponse[];
		return { events };
	} catch (err) {
		console.error('Error loading events (root page):', err);
		return { events: [] as EventResponse[], apiError: 'Backend unavailable' };
	}
};