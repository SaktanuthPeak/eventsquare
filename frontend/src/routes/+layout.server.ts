import { zod } from "sveltekit-superforms/adapters";
import type { LayoutServerLoad } from "./$types";
import { signupSchema } from "./register/schema";
import { superValidate } from "sveltekit-superforms";

export const load: LayoutServerLoad = async ({ locals }) => {
  const SignUpForm = await superValidate(zod(signupSchema));

  return {
    user: locals.user,
  };
};
