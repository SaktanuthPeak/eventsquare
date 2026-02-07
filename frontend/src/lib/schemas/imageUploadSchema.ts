import { z } from 'zod';

export const imageUploadSchema = z.object({
	image: z.instanceof(File)
});
