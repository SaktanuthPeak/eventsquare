import { z } from "zod";
import { eventCategories } from "$lib/static/event";

export const eventSchema = z.object({
  name: z.string().min(1, "Event name is required"),
  description: z.string().min(1, "Event description is required"),
  location: z.string().min(1, "Event location is required"),
  event_type: z.enum(
    eventCategories as [string, ...string[]],
  ),
  startDate: z
    .string()
    .datetime("Invalid datetime format")
    .refine((date) => new Date(date) >= new Date(new Date().setHours(0,0,0,0)), {
      message: "Start date must be in the future",
    }),
  endDate: z
    .string()
    .datetime("Invalid datetime format")
    .refine((date) => new Date(date) >= new Date(new Date().setHours(0,0,0,0)), {
      message: "End date must be in the future",
    }),

  image: z
    .instanceof(File, { message: 'Event image is required' }),

  image_id: z.string().optional(),
  eventStatus: z.enum(["draft", "pending", "active"]).optional().default("active"),
  booking_start_date: z
    .string()
    .datetime("Invalid datetime format")
    .refine((date) => new Date(date) >= new Date(new Date().setHours(0,0,0,0)), {
      message: "Start date must be in the future",
    }),
  booking_end_date: z
    .string()
    .datetime("Invalid datetime format")
    .refine((date) => new Date(date) >= new Date(new Date().setHours(0,0,0,0)), {
      message: "End date must be in the future",
    })
})