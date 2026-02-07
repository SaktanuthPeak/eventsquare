import { fail, redirect } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';
import { checkoutSchema } from './schema';
import { zod } from 'sveltekit-superforms/adapters';
import { superValidate } from 'sveltekit-superforms';
import { bookTickets, getEventById } from '$lib/client';
import { env } from '$env/dynamic/public';

function pickTicketType(
    eventData: any,
    ticketTypeId?: string | null
): { id: string; name: string; price: number; remaining?: number } | null {
    const ticketTypes: any[] = eventData?.ticket_types ?? [];
    if (ticketTypes.length === 0) return null;

    const matchesId = (tt: any): boolean => {
        const id = tt?.ticket_id ?? tt?.id;
        return Boolean(id && ticketTypeId && id === ticketTypeId);
    };

    const selected =
        (ticketTypeId ? ticketTypes.find(matchesId) : null) ??
        ticketTypes[0];

    const resolvedId = selected?.ticket_id ?? selected?.id;
    if (!resolvedId) return null;

    return {
        id: String(resolvedId),
        name: String(selected?.name ?? ''),
        price: Number(selected?.price ?? 0),
        remaining: selected?.remaining != null ? Number(selected.remaining) : undefined
    };
}


export const load: PageServerLoad = async ({ params, url, locals }) => {
    const ticketTypeId = url.searchParams.get('ticketId');
    const quantityParam = url.searchParams.get('quantity');
    const quantityFromUrl = Number(quantityParam ?? '');

    // Must come from the event page selection.
    if (!ticketTypeId || !quantityParam) {
        throw redirect(302, `/events/${params.event}`);
    }

    const initialQuantity = Number.isFinite(quantityFromUrl) && quantityFromUrl > 0 ? quantityFromUrl : NaN;
    if (!Number.isFinite(initialQuantity)) {
        throw redirect(302, `/events/${params.event}`);
    }

    const eventRes = await getEventById({
        client: locals.client,
        path: { event_id: params.event }
    });

    if (!eventRes.response.ok || !eventRes.data) {
        throw redirect(302, '/events');
    }

    let image_url: string | null = null;
    if (eventRes.data?.image_id) {
        const baseUrl = env.PUBLIC_BASE_API_URL || env.PUBLIC_API_URL || 'http://localhost:9000';
        image_url = `${baseUrl}/v1/images/${eventRes.data.image_id}`;
    }
    const selectedTicket = pickTicketType(eventRes.data as any, ticketTypeId);
    if (!selectedTicket) {
        throw redirect(302, `/events/${params.event}`);
    }
    const form = await superValidate(
        {
            event_id: params.event,
            ticket_type_id: selectedTicket.id,
            quantity: initialQuantity
        },
        zod(checkoutSchema as any) as any
    );

    return {
        form,
        eventData: eventRes.data,
        selectedTicket,
        image: image_url
    };
};

export const actions: Actions = {
    default: async (event) => {
        const urlTicketTypeId = event.url.searchParams.get('ticketId');
        const urlQuantityParam = event.url.searchParams.get('quantity');
        const urlQuantity = Number(urlQuantityParam ?? '');

        if (!urlTicketTypeId || !urlQuantityParam || !Number.isFinite(urlQuantity) || urlQuantity <= 0) {
            throw redirect(302, `/events/${event.params.event}`);
        }

        const form = await superValidate(event.request, zod(checkoutSchema as any) as any);
        if (!form.valid) {
            return fail(400, { form });
        }

        // Prevent tampering: checkout must match the selection from the event page.
        if (String((form.data as any).ticket_type_id ?? '') !== String(urlTicketTypeId)) {
            return fail(400, { form, message: 'Ticket selection cannot be changed at checkout' });
        }
        if (Number(form.data.quantity) !== urlQuantity) {
            return fail(400, { form, message: 'Quantity cannot be changed at checkout' });
        }

        const accessToken = event.cookies.get('access_token');
        if (!accessToken) {
            const redirectUrl = new URL('/account/login', event.url);
            redirectUrl.searchParams.set('redirect', event.url.pathname + event.url.search);
            throw redirect(302, redirectUrl);
        }

        const eventRes = await getEventById({
            client: event.locals.client,
            path: { event_id: event.params.event }
        });

        if (!eventRes.response.ok || !eventRes.data) {
            return fail(404, { form, message: 'Event not found' });
        }

        const selectedTicket = pickTicketType(eventRes.data as any, String(urlTicketTypeId));
        if (!selectedTicket) {
            return fail(400, { form, message: 'Invalid ticket type' });
        }

        const quantity = urlQuantity;

        if (
            selectedTicket.remaining != null &&
            Number.isFinite(selectedTicket.remaining) &&
            quantity > selectedTicket.remaining
        ) {
            return fail(400, { form, message: 'Not enough tickets remaining' });
        }

        const pricePerTicket = selectedTicket.price;
        const totalPrice = pricePerTicket * quantity;

        const bookRes = await bookTickets({
            client: event.locals.client,
            headers: { Authorization: `Bearer ${accessToken}` },
            body: {
                event_id: event.params.event,
                ticket_type_id: selectedTicket.id,
                ticket_type_name: selectedTicket.name,
                quantity,
                price_per_ticket: pricePerTicket,
                total_price: totalPrice
            }
        });

        if (!bookRes.response.ok) {
            return fail(400, {
                form,
                message:
                    (Array.isArray((bookRes.error as any)?.errors) && (bookRes.error as any)?.errors?.[0]) ||
                    'Booking failed'
            });
        }

        return { form, type: 'success', booking: bookRes.data ?? null };
    }
};


