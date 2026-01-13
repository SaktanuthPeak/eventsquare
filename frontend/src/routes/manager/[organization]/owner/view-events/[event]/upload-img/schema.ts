import {z} from "zod";

export const uploadImgSchema = z.object({
  image: z
    .instanceof(File)
    .refine((file) => file.size <= 2 * 1024 * 1024, {
      message: "File size must be less than 2MB",
    })
    .refine((file) => file.type.startsWith("image/"), {
      message: "File must be an image",
    }),
});