import { fail, redirect, type Actions } from "@sveltejs/kit";
import { setError, superValidate } from "sveltekit-superforms/server";
import { zod } from "sveltekit-superforms/adapters";
import { organizeSchema } from "./schema";
import type { PageServerLoad } from "./$types";
import { createOrganizer } from "$lib/client";

export const load: PageServerLoad = async (event) => {
  const form = await superValidate(event, zod(organizeSchema));
  return {
    form,
  };
};

export const actions: Actions = {
  default: async ({ request, locals }) => {
    const form = await superValidate(request, zod(organizeSchema));
    const { client } = locals;
    if (!form.valid) {
      return fail(400, { form });
    }

    try {
      const organize_res = await createOrganizer({
        client: client,
        body: {
          name: form.data.name,
          manager_id: locals.user.id,
          co_manager_id: form.data.co_manager_id,
          staffs_id: form.data.staffs_id,
          maximum_event: form.data.maximum_event,
          contact_information: {
            email: form.data.contact_information.email,
            line_id: form.data.contact_information.line_id,
            facebook: form.data.contact_information.facebook,
            instagram: form.data.contact_information.instagram,
            website_url: form.data.contact_information.website_url,
          },
          business_address: {
            company_name: form.data.business_address.company_name,
            company_address: form.data.business_address.company_address,
            company_phone: form.data.business_address.company_phone,
          },
          banking_information: {
            bank_name: form.data.banking_information.bank_name,
            account_number: form.data.banking_information.account_number,
            account_name: form.data.banking_information.account_name,
          },
        },
      });

      if (!organize_res.response.ok) {
        return fail(organize_res.response.status, {
          form,
          type: "error",
          message:
            organize_res.error?.errors?.[0] || "Failed to create organizer",
        });
      }

      return {
        form,
        type: "success",
        message: "Organizer created successfully",
      };
    } catch (e) {
      console.log(e);
      return setError(form, "name", `${e}`);
    }
  },
};
