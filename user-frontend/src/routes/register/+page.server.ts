 import { fail, redirect, type Actions } from "@sveltejs/kit";
import { setError, superValidate } from "sveltekit-superforms/server";
import { zod } from "sveltekit-superforms/adapters";
import { signupSchema } from "./schema";
import type { PageServerLoad } from "./$types";
import { create } from "$lib/client";

export const load: PageServerLoad = async (event) => {
  const form = await superValidate(event, zod(signupSchema));
  return {
    form,
  };
};

export const actions: Actions = {
  default: async (request) => {
    const form = await superValidate(request, zod(signupSchema));

    if (!form.valid) {
      return fail(400, { form });
    }

    try {
      const signup_res = await create({
        client: request.locals.client,
        body: {
          email: form.data.email,
          username: form.data.username,
          password: form.data.password,
          confirm_password: form.data.confirm_password,
          status: "active",
          first_name: form.data.first_name,
          last_name: form.data.last_name,
        },
      });
      
      if (!signup_res.response.ok) {
        return fail(signup_res.response.status, {
          form,
          type: "error",
          error: signup_res.error?.errors?.[0] ?? "An error occurred during signup",
        });
      }

      return{
        form,
        type: "success",
      }

    } catch (e) {
      console.log(e);
      return setError(form, "username", `${e}`);
    } 
    // finally {
    //   throw redirect(302, "/");
    // }
  },
};