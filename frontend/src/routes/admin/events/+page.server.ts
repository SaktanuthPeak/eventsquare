import { deleteEvent, getEvents, type EventResponse } from '$lib/client';
import type { Actions, PageServerLoad } from './$types';
import { fail } from '@sveltejs/kit';

export const load: PageServerLoad = async ({ locals, url }) => {
	const page = Number(url.searchParams.get('page') || 1);
	const size = Number(url.searchParams.get('size') || 25);
	const search = url.searchParams.get('search') || '';

	try {
		const res = await getEvents({
			client: locals.client,
			query: {
				page,
				size,
				...(search ? { name: search } : {})
			}
		});

		const items = (res.data?.items ?? []) as EventResponse[];
		return {
			events: items,
			total: res.data?.total ?? null,
			page: res.data?.page ?? page,
			size: res.data?.size ?? size,
			search
		};
	} catch (err) {
		console.error('Error loading admin events:', err);
		return { events: [], total: 0, page, size, search };
	}
};

export const actions: Actions = {
	delete: async ({ request, locals, cookies }) => {
		const formData = await request.formData();
		const eventIdValue = formData.get('event_id');
		const eventId = typeof eventIdValue === 'string' ? eventIdValue : '';

		if (!eventId) {
			return fail(400, { success: false, message: 'Event ID is required' });
		}

		const accessToken = cookies.get('access_token');
		if (!accessToken) {
			return fail(401, { success: false, message: 'Not authenticated' });
		}

		try {
			const res = await deleteEvent({
				client: locals.client,
				headers: { Authorization: `Bearer ${accessToken}` },
				path: { event_id: eventId }
			});

			if (!res.response.ok) {
				const message = (res.error as any)?.detail || (res.error as any)?.message || 'Failed to delete event';
				return fail(res.response.status || 500, { success: false, message });
			}
			return { success: true, message: 'Event deleted successfully' };
		} catch (err) {
			console.error('Error deleting event:', err);
			return fail(500, { success: false, message: 'Failed to delete event' });
		}
	}
};
