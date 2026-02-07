import { getEvents, type EventResponse } from '$lib/client';
import type { PageServerLoad } from './$types';

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
