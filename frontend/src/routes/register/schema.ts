import { z } from "zod";

export const signupSchema = z
  .object({
    email: z.string().email("Email is invalid"),
    username: z.string().min(5, "Username must be at least 5 characters"),
    password: z.string().min(6, "Password must be at least 6 characters"),
    status: z.enum(["active", "inactive"]),
    confirm_password: z.string(),
    first_name: z.string().default(""),
    last_name: z.string().default(""),
  })
  .refine((data) => data.password === data.confirm_password, {
    message: "Passwords do not match",
    path: ["confirm_password"],
  });
