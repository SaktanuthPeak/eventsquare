import type { Actions, PageServerLoad } from './$types';
import { fail } from '@sveltejs/kit';
import { superValidate, withFiles } from 'sveltekit-superforms/server';
import { zod } from 'sveltekit-superforms/adapters';
import { eventFormSchema } from '$lib/schemas/eventSchema';
import { getEventById } from '$lib/client';
import { env } from '$env/dynamic/public';
import { eventCategories } from '$lib/static/event';
import type { z } from 'zod';

const editEventAdapter = zod(eventFormSchema as any) as any;

function toIsoString(value: unknown): string {
	const dt = new Date(value as any);
	return Number.isNaN(dt.getTime()) ? new Date().toISOString() : dt.toISOString();
}

export const load: PageServerLoad = async ({ params, locals }) => {
	const eventId = params.id;

	const res = await getEventById({
		client: locals.client,
		path: { event_id: eventId }
	});

	const event = res.data;
	if (!event) {
		return { form: await superValidate<z.infer<typeof eventFormSchema>>(editEventAdapter), event: null };
	}

	const safeEventType = eventCategories.includes((event.event_type ?? '') as any)
		? (event.event_type as any)
		: 'other';

	const defaults = {
		name: event.name ?? '',
		description: event.description ?? '',
		location: event.location ?? '',
		event_type: safeEventType,
		start_date: toIsoString(event.start_date),
		end_date: toIsoString(event.end_date),
		booking_start_date: toIsoString(event.booking_start_date),
		booking_end_date: toIsoString(event.booking_end_date),
		image_id: event.image_id ?? undefined,
		eventStatus: 'active'
	};

	const form = await superValidate<z.infer<typeof eventFormSchema>>(defaults as any, editEventAdapter);
	return { form, event };
};

export const actions: Actions = {
	default: async (event) => {
		const form = await superValidate<z.infer<typeof eventFormSchema>>(event, editEventAdapter);
		if (!form.valid) {
			return fail(400, { ...withFiles({ form }) });
		}

		const accessToken = event.cookies.get('access_token');
		if (!accessToken) {
			return fail(401, { ...withFiles({ form }), message: 'Not authenticated' });
		}

		const eventId = event.params.id;

		let startDateISO = new Date((form.data as any).start_date);
		startDateISO.setUTCHours(0, 0, 0, 0);
		let endDateISO = new Date((form.data as any).end_date);
		endDateISO.setUTCHours(23, 59, 59, 999);
		let bookingStartDate = new Date(form.data.booking_start_date);
		bookingStartDate.setUTCHours(0, 0, 0, 0);
		let bookingEndDate = new Date(form.data.booking_end_date);
		bookingEndDate.setUTCHours(23, 59, 59, 999);

		try {
			const baseUrl = env.PUBLIC_BASE_API_URL || 'http://localhost:9000';
			const updateUrl = new URL(`/v1/events/${eventId}`, baseUrl);

			const updateRes = await fetch(updateUrl, {
				method: 'PUT',
				headers: {
					Authorization: `Bearer ${accessToken}`,
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					name: form.data.name,
					description: form.data.description?.trim() ? form.data.description : null,
					event_type: form.data.event_type,
					location: form.data.location?.trim() ? form.data.location : null,
					start_date: startDateISO,
					end_date: endDateISO,
					booking_start_date: bookingStartDate,
					booking_end_date: bookingEndDate
				})
			});

			if (!updateRes.ok) {
				const text = await updateRes.text().catch(() => '');
				return fail(400, { ...withFiles({ form }), message: text || 'Failed to update event' });
			}

			const imageFile = (form.data as any).image as File | undefined;
			if (imageFile instanceof File) {
				const uploadUrl = new URL('/v1/images/upload', baseUrl);
				uploadUrl.searchParams.set('event_id', eventId);

				const body = new FormData();
				body.set('file', imageFile);

				const uploadRes = await fetch(uploadUrl, {
					method: 'POST',
					headers: {
						Authorization: `Bearer ${accessToken}`
					},
					body
				});

				if (!uploadRes.ok) {
					return fail(400, { ...withFiles({ form }), message: 'Image upload failed' });
				}
			}

			return { ...withFiles({ form }), type: 'success' };
		} catch (err) {
			console.error('Error updating event:', err);
			return fail(500, { ...withFiles({ form }), message: 'Internal error updating event' });
		}
	}
};
