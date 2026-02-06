import {
    getUserProfile,
    refreshAccessToken,
    constructCookieOptions
} from '$lib/utils/auth';
import { error, redirect, type Handle } from '@sveltejs/kit';

function isProtectedRoute(url: string | null) {
    if (!url) return false;
    return url.split('/').includes('(protected)');
}

function isProtectedApi(url: string | null) {
    if (!url) return false;
    return url.includes('/api/(protected)');
}

export const handleUserAuth: Handle = async ({ event, resolve }) => {
    const { cookies, locals, route, params, url } = event;

    if (cookies.get('refresh_token')) {
        if (!cookies.get('access_token')) {
            console.log("access_token was expired")
            try {
                await refreshAccessToken(event.cookies);
            } catch (err) {
                console.log('errror refresh token', err);
                cookies.delete('access_token', constructCookieOptions(0));
                cookies.delete('refresh_token', constructCookieOptions(0));
            }
        }

        try {
            locals.user = await getUserProfile(cookies.get('access_token') ?? null);
        } catch (err) {
            console.error('error hook get user profile', err);
        }
        locals.token = cookies.get('access_token') ?? undefined;
    }

    if (route.id && isProtectedApi(route.id) && !locals.user) {
        error(401, {
            message: 'Unauthorized'
        });
    }

    if (route.id && isProtectedRoute(route.id) && !locals.user) {
        redirect(
            302,
            `/account/login?redirect_from=${encodeURIComponent(url.pathname)}`
        );
    }

    // not sure, read from this guide https://docs.directus.io/blog/directus-auth-sveltekit.html#create-the-login-form
    // this is needed so that the response headers from SvelteKit do include the correct header to allow the browser to parse json requests
    try {
        return await resolve(event, {
            filterSerializedResponseHeaders: (key) => {
                return key.toLowerCase() === 'content-type';
            }
        });
    } catch (err) {
        console.error('error hooks resolve =>', err);
        error(500, 'Internal server error');
    }
};