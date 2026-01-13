import {z} from 'zod';

export const deleteEventSchema = z.object({
  eventId: z.string(),
});