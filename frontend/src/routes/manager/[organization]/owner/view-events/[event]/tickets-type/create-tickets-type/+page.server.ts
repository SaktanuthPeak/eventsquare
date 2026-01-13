import { fail, superValidate } from "sveltekit-superforms";
import type { PageServerLoad, RequestEvent } from "./$types";
import { createETicketSchema } from "./schema";
import { zod } from "sveltekit-superforms/adapters";
import { createTicketType } from "$lib/client";

export const load: PageServerLoad = async (event) => {
  const form = await superValidate(zod(createETicketSchema));
  return {
    form,
    organization_id: event.params.organization,
    event_id: event.params.event,
  };
};

export const actions = {
  default: async ({ locals,request, params }) => {
    const form = await superValidate(request, zod(createETicketSchema));
    const {client} = locals;

    if (!form.valid) {
      return fail(400, { form });
    }

    try {
      const res = await createTicketType({
        client: client,
        body: {
          name: form.data.name,
          description: form.data.description,
          event_id: params.event,
          ticket_status: form.data.ticket_status,
          price: form.data.price,
          audience_quantity: form.data.audienceQuantity,
          quantity_remaining: form.data.audienceQuantity,
          max_per_user: form.data.maxPerUser,
          allowed_dates: (form.data.allowedDates || []).map(
            (dateStr) => new Date(dateStr)
          ),
        },
      });

      if (!res.response.ok) {
        return fail(500, {
          form,
          error: "Failed to create ticket type",
        });
      }

      // Return success with data
      return {
        form,
        success: true,
        message: "Ticket created successfully",
      };
    } catch (error) {
      console.error("Error creating ticket:", error);
      return fail(500, {
        form,
        error: "Server error creating ticket",
      });
    }
  },
};
