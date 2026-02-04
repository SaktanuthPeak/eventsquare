import { z } from 'zod';

export const loginSchema = z.object({
	username: z.string().min(5, 'Invalid Username'),
	password: z.string().min(6, 'Password must be at least 6 characters long')
});