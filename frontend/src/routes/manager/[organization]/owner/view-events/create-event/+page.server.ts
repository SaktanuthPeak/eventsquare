import type { Actions, PageServerLoad } from "./$types";
import { message, superValidate, withFiles } from "sveltekit-superforms/server";
import { zod } from "sveltekit-superforms/adapters";
import { createEventSchema } from "./schema";
import { createEvent } from "$lib/client";
import { fail } from "@sveltejs/kit";
import { uploadImage } from "$lib/client";

export const load = (async ({ params }) => {
  const form = await superValidate(zod(createEventSchema));
  return { form };
}) satisfies PageServerLoad;


export const actions: Actions = {
  default: async ( event ) => {
    const form = await superValidate(event, zod(createEventSchema));
    const {client} = event.locals;

    if (!form.valid) {
      return fail(400, {
        ...withFiles({ form }),
        type: "error",
      });
    }

    let startDateISO = new Date(form.data.startDate).setUTCHours(0, 0, 0, 0);
    let endDateISO = new Date(form.data.endDate).setUTCHours(23, 59, 59, 999);
    try {
      const createEventRes = await createEvent({
        client: client,
        body: {
          title: form.data.title,
          description: form.data.description,
          organizer_id: event.params.organization,
          event_type: form.data.event_type,
          event_category: form.data.event_category,
          max_audience: form.data.maxAudience,
          start_date: new Date(startDateISO),
          end_date: new Date(endDateISO),
          location: form.data.location,
          event_status: "active",
          check_in_range: form.data.checkInRange.map((range) => ({
            start_time: range.start_time,
            end_time: range.end_time,
          })),
        },
      });

      if (!createEventRes.response.ok ) {
        return fail(400, {
          ...withFiles({ form }),
          type: "error",
          message: createEventRes.error?.errors?.[0] || "Failed to create event",
        });
      }

      const uploadRes = await uploadImage({
        client: client,
        headers: {
            Authorization: `Bearer ${event.cookies.get('access_token')}`,
        },
        path: {
            event_id: createEventRes.data?.id || "",
        },
        body: {
            file: form.data.image,
        },
      })

      if (!uploadRes.response.ok) {
        console.error("Image upload failed:", uploadRes);
        return {
          ...withFiles({ form }),
          type: "error",
        };
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
