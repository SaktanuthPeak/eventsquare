import {z} from 'zod';

export const selectTicketSchema = z.object({
    ticket_id: z.string(),
})