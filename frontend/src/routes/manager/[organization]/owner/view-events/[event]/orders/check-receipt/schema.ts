import {z} from 'zod';

export const checkReceiptSchema = z.object({
    order_id : z.string().min(1, {message: 'Order ID is required'}),
    action : z.enum(['approve','disapprove'])
})