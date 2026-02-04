import { redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import { checkoutSchema } from './schema';
import { zod } from 'sveltekit-superforms/adapters';
import { fail, superValidate } from 'sveltekit-superforms';


export const load = (async (params) => {
    const form = await superValidate(zod(checkoutSchema))

    return {form,

    };
}) satisfies PageServerLoad;


