import { z } from "zod";
import { eventCategories } from "$lib/static/event";

const emptyStringToNull = (value: unknown) => {
  if (typeof value === 'string' && value.trim().length === 0) return null;
  return value;
};

const ticketTypesFromForm = (value: unknown) => {
  // HTML forms will submit hidden JSON as string; accept array/null too.
  if (value === undefined) return undefined;
  if (value === null) return null;
  if (Array.isArray(value)) return value;
  if (typeof value === 'string') {
    const trimmed = value.trim();
    if (trimmed.length === 0) return [];
    try {
      return JSON.parse(trimmed);
    } catch {
      return value;
    }
  }
  return value;
};

export const ticketTypeInputSchema = z.object({
  name: z.string().min(1),
  total: z.number().int().positive(),
  price: z.number().nonnegative(),
  remaining: z.number().int().nonnegative().optional()
});

// Matches Swagger/OpenAPI EventCreate shape
export const eventCreateSchema = z.object({
  name: z.string().min(1, 'Event name is required'),
  description: z.preprocess(emptyStringToNull, z.string().nullable()),
  event_type: z.enum(eventCategories as [string, ...string[]]),
  location: z.preprocess(emptyStringToNull, z.string().nullable()).optional(),
  ticket_types: z.preprocess(
    ticketTypesFromForm,
    z.array(ticketTypeInputSchema).nullable().optional()
  ),
  start_date: z.string().datetime('Invalid datetime format'),
  end_date: z.string().datetime('Invalid datetime format'),
  booking_start_date: z.string().datetime('Invalid datetime format'),
  booking_end_date: z.string().datetime('Invalid datetime format')
});

export const eventFormSchema = z.object({
  name: z.string().min(1, 'Event name is required'),
  description: z.string().optional().default(''),
  event_type: z.enum(eventCategories as [string, ...string[]]),
  location: z.string().optional().default(''),
  ticket_types: z.preprocess(ticketTypesFromForm, z.array(ticketTypeInputSchema).nullable().optional()).default('[]'),
  start_date: z.string().datetime('Invalid datetime format'),
  end_date: z.string().datetime('Invalid datetime format'),
  booking_start_date: z.string().datetime('Invalid datetime format'),
  booking_end_date: z.string().datetime('Invalid datetime format'),
  image_id: z.string().optional(),
  eventStatus: z.enum(['draft', 'pending', 'active']).optional().default('active')
});

export const eventSchema = eventFormSchema;