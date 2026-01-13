import {z} from "zod";

export const scanPageSchema = z.object({
    qrCode: z.string().min(1, "QR Code is required"),
})