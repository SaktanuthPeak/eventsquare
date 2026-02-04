import { z } from 'zod';

export const userSchema = z
.object({
        email: z.string().email('อีเมลไม่ถูกต้อง').min(1, 'อีเมลจำเป็นต้องระบุ'),
		username: z.string().min(5, 'ชื่อผู้ใช้ต้องมีอย่างน้อย 5 ตัวอักษร'),
		first_name: z.string().min(1, 'ชื่อจริงจำเป็นต้องระบุ'),
		last_name: z.string().min(1, 'นามสกุลจำเป็นต้องระบุ'),
		password: z.string().min(6, 'รหัสผ่านต้องมีอย่างน้อย 6 ตัวอักษร'),
        status: z.enum(['active', 'inactive']), 
		confirm_password: z.string().min(6, 'ยืนยันรหัสผ่านต้องมีอย่างน้อย 6 ตัวอักษร'),
	})
	.refine((data) => data.password === data.confirm_password, {
		message: 'รหัสผ่านไม่ตรงกัน'
	});

export const updateUserSchema = z.object({
	first_name: z.string().min(1, 'ชื่อจริงจำเป็นต้องระบุ'),
	last_name: z.string().min(1, 'นามสกุลจำเป็นต้องระบุ'),
	email: z.string().email('อีเมลไม่ถูกต้อง').min(1, 'อีเมลจำเป็นต้องระบุ'),
	phone_number: z
		.string()
		.min(10, 'เบอร์โทรศัพท์ต้องมี 10 หลัก')
		.regex(/^\d+$/, 'เบอร์โทรศัพท์ต้องเป็นตัวเลขเท่านั้น'),
	username: z.string().min(5, 'ชื่อผู้ใช้ต้องมีอย่างน้อย 5 ตัวอักษร'),
	roles: z
		.enum(['admin', 'creator'], {
			errorMap: () => ({ message: 'บทบาทผู้ใช้ไม่ถูกต้อง' })
		})
		.default('creator'),
	company: z.string().optional()
})