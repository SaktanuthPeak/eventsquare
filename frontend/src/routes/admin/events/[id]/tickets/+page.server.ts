import type { Actions, PageServerLoad } from './$types';
import { getEventById,  } from '$lib/client';


export const load: PageServerLoad = async ({ params, locals }) => {
	const res = await getEventById({
		client: locals.client,
		path: { event_id: params.id }
	});

	return {
		event: res.data ?? null
	};
};
