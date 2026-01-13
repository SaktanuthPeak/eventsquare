import { fail, redirect, type Actions } from "@sveltejs/kit";
import { setError, superValidate } from "sveltekit-superforms/server";
import { zod } from "sveltekit-superforms/adapters";
import { organizeSchema } from "../../../create-organizer/schema";
import type { PageServerLoad } from "./$types";
import { updateOrganizer, getOrganizerCompleteInfo } from "$lib/client";

export const load: PageServerLoad = async ({ locals,url }) => {
  const form = await superValidate(zod(organizeSchema));
  const { client } = locals;
  // Get ID from URL query parameter
  const organizerId = url.searchParams.get("id");

  if (organizerId) {
    try {
      const organizerData = await getOrganizerCompleteInfo({
        client: client,
        path: { organizer_id: organizerId },
      });

      const form = {
        name: organizerData.data?.organizer.name || "",
        maximum_event: organizerData.data?.organizer.maximum_event || 3,
        contact_information: {
          email: organizerData.data?.organizer.contact_information?.email || "",
          line_id:
            organizerData.data?.organizer.contact_information?.line_id || "",
          facebook:
            organizerData.data?.organizer.contact_information?.facebook || "",
          instagram:
            organizerData.data?.organizer.contact_information?.instagram || "",
          website_url:
            organizerData.data?.organizer.contact_information?.website_url ||
            "",
        },
        business_address: {
          company_name:
            organizerData.data?.organizer.business_address?.company_name || "",
          company_address:
            organizerData.data?.organizer.business_address?.company_address ||
            "",
          company_phone:
            organizerData.data?.organizer.business_address?.company_phone || "",
        },
        banking_information: {
          bank_name:
            organizerData.data?.organizer.banking_information?.bank_name || "",
          account_number:
            organizerData.data?.organizer.banking_information?.account_number ||
            "",
          account_name:
            organizerData.data?.organizer.banking_information?.account_name ||
            "",
        },
      };

      return {
        form,
        organizer: organizerData.data,
        organization_id: organizerId,
      };
    } catch (error) {
      console.error("Failed to load organizer:", error);
    }
  }

  return { form };
};

export const actions: Actions = {
  default: async ({ locals,request, url }) => {
    const formData = await request.formData();
    const { client } = locals;
    const organizerId = url.searchParams.get("id");

    const form = await superValidate(formData, zod(organizeSchema));

    if (!organizerId) {
      return setError(form, "", "Missing organizer ID");
    }

    if (!form.valid) {
      return fail(400, { form });
    }

    try {
      const result = await updateOrganizer({
        client: client,
        path: { organizer_id: organizerId },
        body: {
          name: form.data.name,
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

      if (!result.response.ok) {
        return fail(result.response.status, {
          form,
          type: "error",
          message: result.error?.errors?.[0] || "Failed to create organizer",
        });
      }

      return {
        form,
        success: true,
        type: "success",
        message: "Organizer updated successfully",
      };
    } catch (e) {
      console.error(e);
      return setError(form, "name", `${e}`);
    }
  },
};
