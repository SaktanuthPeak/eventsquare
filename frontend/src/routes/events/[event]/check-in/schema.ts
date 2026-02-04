import { z } from "zod";

export const checkInSchema = z.object({
  eventId: z.string(),
})