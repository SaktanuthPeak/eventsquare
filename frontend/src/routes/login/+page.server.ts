import type { Actions, PageServerLoad } from './$types';
import { env } from '$env/dynamic/private';
import { error, fail, redirect } from '@sveltejs/kit';
import { superValidate } from 'sveltekit-superforms/server';
import { zod } from 'sveltekit-superforms/adapters';
import { loginSchema } from './loginSchema';
import { authentication } from '$lib/client';


export const load = (async (event) => {
  const form = await superValidate(event,zod(loginSchema));
  return { form };
}) satisfies PageServerLoad;

export const actions = {
  default: async ({ locals,request,cookies }) => {
    const form = await superValidate(request , zod(loginSchema))
    const { client } = locals;

    if (!form.valid){
      return{
        form,errors:form.errors
      }
    }

    try{
      const res = await authentication({
        client: client,
        body: {
          username: form.data.username,
          password: form.data.password
        }
      });

      if (!res.response.ok) {
        return fail(401,{
          form,
          type: 'failure',
          errors:  Array.isArray(res.error?.errors) && res.error?.errors.length > 0
            ? res.error.errors[0]
            : 'Login failed. Please check your credentials.',
        });
      }

      const access_token = res.data?.access_token;

      if (!access_token) {
        return { 
          form,
          type: error,
          errors: 'Login failed. Please check your credentials.' };
      }

      cookies.set('access_token', access_token, {
        path: '/',
        httpOnly: true,
        sameSite: 'strict',
        secure: env.SECURE === 'true',
        maxAge: 60 * 60 * 24 * 30
      });
      
      return {
        form,
        type: 'success',
      }
    }catch(error){
      return{
        status:500,
        errors: 'An unexpected error occurred. Please try again.',
        form: form
      }
    }
  },
} satisfies Actions;