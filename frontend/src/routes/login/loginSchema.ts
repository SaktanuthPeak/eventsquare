import { z } from "zod";

export const loginSchema = z.object({
  username: z.string().min(5 , 'Username is required'),
  password: z.string().min(6 , 'Password must be at least 6 character')
})