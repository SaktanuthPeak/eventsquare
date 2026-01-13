import { fail, superValidate } from "sveltekit-superforms";
import type { PageServerLoad } from "./$types";
import { uploadImgSchema } from "./schema";
import { zod } from "sveltekit-superforms/adapters";
import { uploadImage } from "$lib/client";

export const load = (async (event) => {
  const form = await superValidate(event, zod(uploadImgSchema));
  return { form };
}) satisfies PageServerLoad;

export const actions = {
  default: async (event) => {
    const form = await superValidate(event, zod(uploadImgSchema));
    const { client } = event.locals;
    if (!form.valid) {
      return fail(400, { form });
    }

    try {
      const res = await uploadImage({
        client: client,
        path: {
          event_id: event.params.event,
        },
        body: {
          file: form.data.image,
        },
      });

      if (!res.response.ok) {
        return fail(res.response.status, {
          form,
          error: "Failed to upload image",
        });
      }

      // Return a fresh form instance without the file object
      return {
        form: await superValidate(zod(uploadImgSchema)),
        type: "success",
      };
    } catch (error) {
      console.log("error", error);
      return fail(500, {
        form: await superValidate(zod(uploadImgSchema)),
        error: "An unexpected error occurred",
      });
    }
  },
};
