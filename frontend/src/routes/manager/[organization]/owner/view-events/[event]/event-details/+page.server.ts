import { fail } from "@sveltejs/kit";
import {
  superValidate,
  withFiles,
  type SuperValidated,
} from "sveltekit-superforms/server";
import { zod } from "sveltekit-superforms/adapters";
import { createEventSchema } from "../../create-event/schema";
import { getEventById, partialUpdateEventById, uploadImage } from "$lib/client";
import type { PageServerLoad, Actions } from "./$types";

export const load: PageServerLoad = async ({ locals,params }) => {
  const {client} = locals;
  const eventResponse = await getEventById({
    client: client,
    path: { event_id: params.event },
  });


  const checkInRanges = eventResponse.data?.check_in_range?.map((range : any) => ({
    start_time: range.start_time ? range.start_time.toISOString() : "",
    end_time: range.end_time ? range.end_time.toISOString() : "",
  })) || [];


  const form = await superValidate(
    {
      title: eventResponse.data?.title || "",
      description: eventResponse.data?.description || "",
      location: eventResponse.data?.location || "",
      event_type: eventResponse.data?.event_type || "public",
      startDate: eventResponse.data?.start_date ? new Date(eventResponse.data.start_date).toLocaleString() : "",
      endDate: eventResponse.data?.end_date,
      maxAudience: eventResponse.data?.max_audience || 50,
      checkInRange: checkInRanges,
      event_category: eventResponse.data?.event_category || "other",
      eventStatus: eventResponse.data?.event_status || "draft",
      image: eventResponse.data?.image || null,
    },
    zod(createEventSchema)
  );

  return {
    ...withFiles({ form }),
    start_date: eventResponse.data?.start_date,
    end_date: eventResponse.data?.end_date,
    eventData: eventResponse.data,
    organization_id: params.organization,
    event_id: params.event,
  };
};

export const actions: Actions = {
  default: async (event) => {
    const form = await superValidate(event, zod(createEventSchema));
    const { client } = event.locals;
    if (!form.valid) {
      return {
        ...withFiles({ form }),
        type: "error",
      };
    }

  
    let startDateISO = new Date(form.data.startDate).setUTCHours(0, 0, 0, 0);
    let endDateISO = new Date(form.data.endDate).setUTCHours(23, 59, 59, 999);

    try {
      const result = await partialUpdateEventById({
        client: client,
        path: { event_id: event.params.event },
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
            start_time: new Date(range.start_time),
            end_time: new Date(range.end_time),
          })),
        },
      });

      if (!result.response.ok) {
        return fail(result.response.status, {
          ...withFiles({ form }),
          error: (result.error?.errors && result.error.errors[0]) || "Failed to update event",
        });
      }

      if (!form.data.image?.file_id) {
        const uploadRes = await uploadImage({
          client: client,
          path: {
            event_id: event.params.event || "",
          },
          body: {
            file: form.data.image,
          },
        });

        if (!uploadRes.response.ok) {
          return fail(uploadRes.response.status, {
            ...withFiles({ form }),
            type: "error",
            message: uploadRes.error?.errors?.[0] || "Failed to upload image",
          });
        }
      }

      return { ...withFiles({ form }), type: "success" };
    } catch (error) {
      console.error("Error updating event:", error);
      return fail(500, {
        ...withFiles({ form }),
        error: String(error),
      });
    }
  },
};
