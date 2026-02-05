import { handleUserAuth, isProtectedRoute as isBackOfficeProtectedRoute } from '$lib/server/auth';
import { authHandler } from '$lib/hooks/auth.hook';
import { client } from '$lib/openapiClient';
import { error, type Handle } from '@sveltejs/kit';

export const handle: Handle = async ({ event, resolve }) => {
    // Make the OpenAPI client available server-side for auth + API calls.
    event.locals.client = client;

    const resolveWithFilter: typeof resolve = (evt, opts) => {
        return resolve(evt, {
            ...opts,
            filterSerializedResponseHeaders: (key) => key.toLowerCase() === 'content-type'
        });
    };

    try {
        // Back-office auth (legacy route-group based protection)
        if (isBackOfficeProtectedRoute(event)) {
            return await handleUserAuth({ event, resolve: resolveWithFilter });
        }

        // App user auth (includes /admin role-based protection)
        return await authHandler({ event, resolve: resolveWithFilter });
    } catch (err) {
        console.error('error hooks resolve =>', err);
        throw error(500, 'Internal server error');
    }
};