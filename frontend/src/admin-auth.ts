import {
    getBackOfficeUserProfile,
    refreshAccessToken,
    constructCookieOptions
} from '$lib/utils/admin_auth';
import { error, redirect, type Handle } from '@sveltejs/kit';

function isProtectedRoute(url: string | null) {
    if (!url) return false;
    return url.split('/').includes('admin');
}

function isAuthenticated(cookies: Cookies): boolean {
    return Boolean(cookies.get('back_office_access_token'));
}

export const handleBackOfficeAuth: Handle = async ({ event, resolve }) => {
    const { cookies, locals, route, params, url } = event;

    if (cookies.get('back_office_refresh_token')) {
        if (!cookies.get('back_office_access_token')) {
            console.log("back_office_access_token was expired")
            try {
                await refreshAccessToken(event.cookies);
            } catch (err) {
                console.log('errror refresh token', err);
                cookies.delete('back_office_access_token', constructCookieOptions(0));
                cookies.delete('back_office_refresh_token', constructCookieOptions(0));
            }
        }

        try {
            locals.back_office_user = await getBackOfficeUserProfile(cookies.get('back_office_access_token') ?? null);
        } catch (err) {
            console.error('error hook get user profile', err);
        }
        locals.back_office_token = cookies.get('back_office_access_token') ?? undefined;
    }

    if (route.id && isProtectedRoute(route.id) && !locals.back_office_user) {
        console.log(route.id)
        if (route.id.startsWith('/admin')) {
            redirect(
                302,
                `/${params.lang ?? 'en'}/admin}`
            );
        } else {
            redirect(
                302,
                `/${params.lang ?? 'en'}`
            );
        }
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