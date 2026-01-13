import {z} from 'zod';

export const checkoutSchema = z.object({
    owner_name: z.string().min(1, {message: 'Owner name is required'}),
    co_owner_name: z.string(),
    owner_email: z.string().email({message: 'Invalid email address'}),
    co_owner_email: z.string().email({message: 'Invalid email address'}),
    owner_phone: z.string(),
    co_owner_phone: z.string(),
    audience_per_ticket: z.number(),
    total_amount: z.number(),
    // slip_id: z.any()
    //     .refine((files) => {
    //         return files?.[0] instanceof File;
    //     }, "Please upload a file")
    //     .refine((files) => {
    //         if (!files?.[0]) return false;
    //         return files[0].size <= 10 * 1024 * 1024; // 2MB limit
    //     }, "File size must be less than 10MB")
    //     .refine((files) => {
    //         if (!files?.[0]) return false;
    //         return files[0].type.startsWith('image/');
    //     }, "File must be an image"),
    slip_id: z.instanceof(File),
    event_id: z.string(),
    organizer_id: z.string(),
})