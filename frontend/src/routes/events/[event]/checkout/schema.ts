import {z} from 'zod';

export const checkoutSchema = z.object({
    event_id: z.string().min(1, { message: 'Event is required' }),
    ticket_type_id: z.string().min(1, { message: 'Ticket type is required' }),
    quantity: z.coerce.number().int().min(1).max(10),
})