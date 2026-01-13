import { z } from "zod";

export const createETicketSchema = z.object({
  name: z.string().min(1, { message: "Name is required" }),
  description: z.string().min(1, { message: "Description is required" }),
  event_id: z.string().min(1, { message: "Event ID is required" }),
  ticket_status: z.enum(["avaliable", "disable"]),
  price: z.number().min(0, { message: "Price must be a positive number" }),
  audienceQuantity: z
    .number()
    .min(1, { message: "Quantity must be at least 1" }),
  maxPerUser: z.number().min(1, { message: "Max per user must be at least 1" }),
  allowedDates: z
    .array(z.string().regex(/^\d{4}-\d{2}-\d{2}$/, "Invalid date format"))
    .default([])
    .optional(),
});
