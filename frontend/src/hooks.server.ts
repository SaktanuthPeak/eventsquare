import apiClientHandle from '$lib/hooks/api-client.hook';
import { authHandler } from '$lib/hooks/auth.hook';
import { sequence } from '@sveltejs/kit/hooks';

export const handle = sequence(apiClientHandle, authHandler);