import { create } from '$lib/client';
import { userSchema } from '$lib/schemas/userSchema';
import { superValidate } from 'sveltekit-superforms/server';
import type { Actions, PageServerLoad } from './$types';
import { zod } from 'sveltekit-superforms/adapters';
import { fail } from '@sveltejs/kit';

export const load = (async () => {
    const form = await superValidate(zod(userSchema));
    return { form };
}) satisfies PageServerLoad;

export const actions: Actions = {
    default: async (event) => {
        const form = await superValidate(event, zod(userSchema));

        if (!form.valid) {
            return fail(400, { form });
        }

        const createUserRes = await create({
            client: event.locals.client,
            body: {
                first_name: form.data.first_name,
                last_name: form.data.last_name,
                email: form.data.email,
                status: 'active',
                username: form.data.username,
                password: form.data.password,
                confirm_password: form.data.confirm_password,
                credit: 100000
            }
        });

        if (!createUserRes.response.ok) {
            const statusCode = createUserRes.response.status;
            let errorMessage = 'ไม่สามารถเพิ่มผู้ใช้ได้';

            switch (statusCode) {
                case 400:
                    errorMessage = 'ข้อมูลไม่ถูกต้อง กรุณาตรวจสอบข้อมูลที่กรอก';
                    break;
                case 401:
                case 403:
                    errorMessage = 'ไม่มีสิทธิ์ในการเพิ่มผู้ใช้';
                    break;
                case 404:
                    errorMessage = 'ไม่พบข้อมูลผู้ใช้ที่ต้องการเพิ่ม';
                    break;
                case 409:
                    errorMessage = 'อีเมลนี้ถูกใช้ไปแล้ว';
                    break;
                case 422:
                    errorMessage = 'ข้อมูลไม่ถูกต้องตามเงื่อนไข กรุณาตรวจสอบข้อมูลที่กรอก';
                    break;
                default:
                    errorMessage = `เกิดข้อผิดพลาด (${statusCode}) กรุณาลองใหม่อีกครั้ง`;
            }

            return fail(statusCode, {
                form,
                type: 'error',
                statusCode,
                message: errorMessage
            });
        }

        return {
            form,
            type: 'success',
            message: 'สร้างผู้ใช้สำเร็จ'
        };
    }
};