import { getCheckedInUsers, getEventById } from '$lib/client';
import type { PageServerLoad } from './$types';

export const load = (async ({ locals, params }) => {
    const eventId = params.id;

    const [eventRes, checkinRes] = await Promise.all([
        getEventById({
            client: locals.client,
            path: { event_id: eventId }
        }),
        getCheckedInUsers({
            client: locals.client,
            path: { event_id: eventId }
        })
    ]);

    const participants = (checkinRes.data ?? []).sort(
        (a, b) => new Date(b.check_in_date as any).getTime() - new Date(a.check_in_date as any).getTime()
    );

    return { event: eventRes.data ?? null, participants };
}) satisfies PageServerLoad;