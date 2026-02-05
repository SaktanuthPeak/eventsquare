import type { Actions, PageServerLoad } from "./$types";
import { message, superValidate, withFiles } from "sveltekit-superforms/server";
import { zod } from "sveltekit-superforms/adapters";
import { eventSchema } from "$lib/schemas/eventSchema";
import { createEvent } from "$lib/client";
import { fail } from "@sveltejs/kit";
import { env } from '$env/dynamic/public';
import type { z } from 'zod';

const createEventAdapter = zod(eventSchema as any) as any;

export const load = (async ({ params }) => {
  const form = await superValidate<z.infer<typeof eventSchema>>(createEventAdapter);
  return { form };
}) satisfies PageServerLoad;


export const actions: Actions = {
  default: async ( event ) => {
    const form = await superValidate<z.infer<typeof eventSchema>>(event, createEventAdapter);
    const {client} = event.locals;

    if (!form.valid) {
      return fail(400, {
        ...withFiles({ form }),
        type: "error",
      });
    }

    let startDateISO = new Date(form.data.startDate);
    startDateISO.setUTCHours(0, 0, 0, 0);
    let endDateISO = new Date(form.data.endDate);
    endDateISO.setUTCHours(23, 59, 59, 999);
    let bookingStartDate = new Date(form.data.booking_start_date);
    bookingStartDate.setUTCHours(0,0,0,0);
    let bookingEndDate = new Date(form.data.booking_end_date);
    bookingEndDate.setUTCHours(23,59,59,999);
    try {
      const createEventRes = await createEvent({
        client: client,
        body: {
          name: form.data.name,
          description: form.data.description,
          event_type: form.data.event_type,
          start_date: startDateISO,
          end_date: endDateISO,
        booking_start_date: bookingStartDate,
        booking_end_date: bookingEndDate,
          location: form.data.location,
        },
      });

      if (!createEventRes.response.ok ) {
        return fail(400, {
          ...withFiles({ form }),
          type: "error",
          message: createEventRes.error?.errors?.[0] || "Failed to create event",
        });
      }

      const createdEventId = createEventRes.data?.id;
      const accessToken = event.cookies.get('access_token');
      const imageFile = (form.data as any).image as File | undefined;

      if (createdEventId && accessToken && imageFile instanceof File) {
        const baseUrl = env.PUBLIC_BASE_API_URL || 'http://localhost:9000';
        const uploadUrl = new URL('/v1/images/upload', baseUrl);
        uploadUrl.searchParams.set('event_id', createdEventId);

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
          return fail(400, {
            ...withFiles({ form }),
            type: 'error',
            message: 'Image upload failed'
          });
        }
      }
       
      return {
        ...withFiles({ form }),
        type: "success",
      };
    } catch (error) {
      return {
        status: 500,
        errors: "An unexpected error occurred. Please try again.",
      };
    } 
  },
};