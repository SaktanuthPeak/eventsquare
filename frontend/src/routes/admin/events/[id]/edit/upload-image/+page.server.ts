import type { Actions, PageServerLoad } from './$types';
import { fail } from '@sveltejs/kit';
import { getEventById, uploadImage } from '$lib/client';
import { imageUploadSchema } from '$lib/schemas/imageUploadSchema';
import { superValidate, withFiles } from 'sveltekit-superforms/server';
import { zod } from 'sveltekit-superforms/adapters';

const imageUploadAdapter = zod(imageUploadSchema as any) as any;

export const load: PageServerLoad = async ({ params, locals }) => {
    const res = await getEventById({
        client: locals.client,
        path: { event_id: params.id }
    });

    return {
        event: res.data ?? null,
        form: await superValidate(imageUploadAdapter)
    };
};

export const actions: Actions = {
    default: async (event) => {
        const form = await superValidate(event, imageUploadAdapter);
        if (!form.valid) {
            return fail(400, { ...withFiles({ form }) });
        }

        const accessToken = event.cookies.get('access_token');
        if (!accessToken) {
            return fail(401, { ...withFiles({ form }), message: 'Not authenticated' });
        }

        const imageFile = (form.data as any).image as File;
        const uploadRes = await uploadImage({
            client: event.locals.client,
            headers: { Authorization: `Bearer ${accessToken}` },
            query: { event_id: event.params.id },
            body: { file: imageFile }
        });

        if (!uploadRes.response.ok) {
            return fail(uploadRes.response.status || 400, {
                ...withFiles({ form }),
                message: (uploadRes.error as any)?.errors?.[0] || 'Image upload failed'
            });
        }

        return { ...withFiles({ form }), type: 'success' };
    }
};