import { superValidate } from 'sveltekit-superforms';
import type { PageServerLoad } from './$types';
import { loginSchema } from '$lib/schemas/loginSchema';
import type { Actions } from '@sveltejs/kit';
import { error, fail, redirect } from '@sveltejs/kit';
import { constructCookieOptions } from '$lib/shares/cookies';
import { zod } from 'sveltekit-superforms/adapters';
import { authentication } from '$lib/client';

export const load: PageServerLoad = async ({}) => {
	const form = await superValidate(zod(loginSchema));
	return {
		form
	};
};

export const actions = {
	default: async (context) => {
		const { request, locals, cookies } = context;
		const { client } = locals;
		const form = await superValidate(request, zod(loginSchema));
		if (!form.valid) {
			return { form, errors: form.errors };
		}
		try {
			const loginRes = await authentication({
				client: client,
				body: {
					username: form.data.username,
					password: form.data.password
				}
			});

			if (!loginRes.response.ok) {
				return fail(401, {
					form,
					type: 'failure',
					errors:
						Array.isArray(loginRes.error?.errors) && loginRes.error?.errors.length > 0
							? loginRes.error.errors[0]
							: 'ไม่สามารถเข้าสู่ระบบได้. กรุณาตรวจสอบชื่อผู้ใช้และรหัสผ่านของคุณ.'
				});
			}
			// For example, save the data to a database or send an email

			const access_token = loginRes?.data?.access_token;
			const refresh_token = loginRes?.data?.refresh_token;

			if (!access_token || !refresh_token) {
				return fail(500, {
					form,
					type: 'failure',
					errors: 'ไม่สามารถรับ token ได้ กรุณาลองใหม่อีกครั้ง'
				});
			}

			const accessTokenMaxAge = 60 * 10;
			const refreshTokencookieMaxAge = 60 * 60 * 24 * 10;

			cookies.set('access_token', access_token, constructCookieOptions(accessTokenMaxAge));
			cookies.set('refresh_token', refresh_token, constructCookieOptions(refreshTokencookieMaxAge));

			// You can also redirect or return a success message
			return {
				form,
				success: true,
				message: 'เข้าสู่ระบบสำเร็จ'
			};
		} catch (error) {
			console.error('มีข้อผิดพบาดระหว่างเข้าสู่ระบบ:', error);
			return {
				status: 500,
				errors: 'เกิดข้อผิดพลาดในการเข้าสู่ระบบ กรุณาลองใหม่อีกครั้ง',
				form: form
			};
		}
	}
} satisfies Actions;