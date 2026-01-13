import { superValidate } from "sveltekit-superforms";
import type { PageServerLoad } from "./$types";
import { scanPageSchema } from "./schema";
import { zod } from "sveltekit-superforms/adapters";
import { fail } from "@sveltejs/kit";

export const load = (async (event) => {
  const form = await superValidate(event, zod(scanPageSchema));
  return { form };
}) satisfies PageServerLoad;

export const actions = {
  default: async ({ request }) => {
    const form = await superValidate(request, zod(scanPageSchema));

    if (!form.valid) {
      return fail(400, { form });
    }

    try {
      // add logic for processing QR code
      return {
        form,
        type: "success",
      };
    } catch (error) {
      console.error("Error:", error);
      return fail(500, {
        form,
        error: "Failed to process QR code",
      });
    }
  },
};
