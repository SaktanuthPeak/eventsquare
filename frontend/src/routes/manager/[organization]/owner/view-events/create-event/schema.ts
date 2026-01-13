import { string, z } from "zod";
import { eventCategories } from "$lib/static/event";

const checkInRangeSchema = z.object({
  start_time: z
    .string()
    .datetime("Invalid datetime format")
    .refine((date) => new Date(date) >= new Date(new Date().setHours(0,0,0,0)), {
      message: "Start time cannot be in the past",
    }),
  end_time: z
    .string()
    .datetime("Invalid datetime format")
    .refine((date) => new Date(date) >= new Date(new Date().setHours(0,0,0,0)), {
      message: "End time cannot be in the past",
    })
  })
   .refine((data) => new Date(data.start_time) < new Date(data.end_time), {
    message: "Start date cannot be later than end date",
    path: ["end_date"],
  });

export const createEventSchema = z.object({
  title: z.string().min(1, "Event name is required"),
  description: z.string().min(1, "Event description is required"),
  location: z.string().min(1, "Event location is required"),
  event_type: z.enum(["public", "private"]),
  event_category: z.enum(
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
  image: z.union([
    z.instanceof(File),
    z.object({
      file_id: z.string(),
      filename: z.string(),       
      content_type: z.string(),   
    }),
    z.null(),
    z.undefined()
  ])
    .refine((file) =>  file instanceof File ? file.size <= 10 * 1024 * 1024 : true, {
      message: "File size must be less than 10MB",
    })
    .refine((file) => file instanceof File ? file.type.startsWith("image/") : true, {
      message: "File must be an image",
    }).optional(),
  maxAudience: z.number().min(1, "Maximum audience is required"),
  eventStatus: z.enum(["draft", "pending", "active"]),
  checkInRange: z.array(checkInRangeSchema).optional().default([])
}).refine((data) => new Date(data.startDate) <= new Date(data.endDate), {
  message: "Start date cannot be later than end date",
}).refine((data) => data.checkInRange.every(range => new Date(range.start_time) <= new Date(range.end_time)), {
  message: "Start time cannot be later than end time in check-in range",
})
.refine((data) => {
  if (
    !Array.isArray(data.checkInRange) ||
    !data.startDate ||
    !data.endDate
  ) return false;

  const startDate = new Date(data.startDate);
  startDate.setHours(0, 0, 0, 0);
  const endDate = new Date(data.endDate);
  endDate.setHours(23, 59, 59, 999);
  return data.checkInRange.every(range => {
    const rangeStart = new Date(range.start_time);
    const rangeEnd = new Date(range.end_time);
    return rangeStart >= startDate && rangeEnd <= endDate;
  });
},{
    message: "Check-in range must be within event start and end dates",
    path: ["checkInRange"],
})

