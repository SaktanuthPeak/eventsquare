import { PUBLIC_API_URL } from '$env/static/private';
import type { Cookies } from '@sveltejs/kit';
import type { JwtPayload } from 'jwt-decode';

export const getUserProfile = async (access_token: string | null) => {
    try {
        const response = await fetch(`${PUBLIC_API_URL}/api/v1/auth/me`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${access_token}`
            },
        })

        if (response.status == 200) {
            const data = await response.json();
            return data;
        }
    } catch (e) {
        console.error('error get user profile:', e);
        return null;
    }
    return null;
};

export function saveToken(cookies: Cookies, accessToken: string, accessTokenExpires: string, refreshToken: string, refreshTokenExpires: string) {
    const now: Date = new Date();
    const access_token_expires: Date = new Date(accessTokenExpires);
    const access_token_max_age: number = Math.floor((access_token_expires.getTime() - now.getTime()) / 1000) - 30;
    // set access token expires 30 second early.

    const refresh_token_expires = new Date(refreshTokenExpires);
    const refresh_token_max_age: number = Math.floor((refresh_token_expires.getTime() - now.getTime()) / 1000) - 30;
    // set refresh token expires 30 second early.

    cookies.set('access_token', accessToken, constructCookieOptions(access_token_max_age));
    cookies.set('refresh_token', refreshToken, constructCookieOptions(refresh_token_max_age));
}

export async function refreshAccessToken(cookies: Cookies) {
    if (cookies.get('refresh_token')) {
        try {
            // use refresh token
            const response = await fetch(`${PUBLIC_API_URL}/api/v1/auth/refresh_token`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    'grant_type': 'refresh_token',
                    'refresh_token': cookies.get('refresh_token')
                })
            })

            if (response.status != 200) {
                cookies.delete('access_token', constructCookieOptions(0));
                cookies.delete('refresh_token', constructCookieOptions(0));
            } else {
                const data = await response.json();
                saveToken(cookies, data.access_token, data.access_token_expires, data.refresh_token, data.refresh_token_expires);
            }
        } catch (error) {
            cookies.delete('access_token', constructCookieOptions(0));
            cookies.delete('refresh_token', constructCookieOptions(0));
        }
    }
}

export const constructCookieOptions: {
    (expires: number): {
        path: string;
        httpOnly: boolean;
        sameSite: boolean | 'lax' | 'strict' | 'none';
        secure: boolean;
        maxAge: number;
    };
} = (expires: number) => {
    return {
        // send cookie for every page
        path: '/',

        // server side only cookie so you can't use `document.cookie`
        httpOnly: true,

        // only requests from same site can send cookies
        sameSite: 'strict',

        // only sent over HTTPS in production
        secure: process.env.NODE_ENV === 'production',

        // set cookie to expire after a given time
        maxAge: expires
    };
};