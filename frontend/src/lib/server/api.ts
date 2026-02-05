import { error, isRedirect, redirect, type RequestEvent } from '@sveltejs/kit';
import { ACCESS_TOKEN_COOKIE_NAME } from './global';
import { PUBLIC_API_URL } from '$env/static/public';

const DEFAULT_PAGE_SIZE = 10;

const API_ENDPOINT = PUBLIC_API_URL;

export type IPaginate<T> = {
	items: T[];
	total: number;
	page: number;
	size: number;
};

interface FetchResponse<T = unknown> {
	data?: T;
	error?: string;
	response?: Response;
	status?: number;
	headers?: Headers;
}

export function objectToQueryString(obj: Record<string, string | number | boolean | null>): string {
	const params = [];
	for (const key in obj) {
		if (Object.prototype.hasOwnProperty.call(obj, key)) {
			if (obj[key] === null || obj[key] === undefined || obj[key] === '') continue; // Skip null or undefined values
			const encodedKey = encodeURIComponent(key);
			const encodedValue = encodeURIComponent(obj[key]);
			params.push(`${encodedKey}=${encodedValue}`);
		}
	}
	return params.join('&');
}

export async function apiFetch<T>(
	event: RequestEvent,
	endpoint: string,
	requestInit: RequestInit = {},
	options: {
		omitContentTypeHeader?: boolean;
	} = {}
): Promise<FetchResponse<T>> {
	// Default headers
	const defaultHeaders: HeadersInit = {};

	if (!options.omitContentTypeHeader) {
		defaultHeaders['Content-Type'] = 'application/json';
	}

	const accessToken = event.cookies.get(ACCESS_TOKEN_COOKIE_NAME);
	if (accessToken) {
		defaultHeaders['Authorization'] = `Bearer ${accessToken}`;
	}

	const config: RequestInit = {
		headers: { ...defaultHeaders, ...requestInit.headers },
		...requestInit
	};

	try {
		const res = await event.fetch(API_ENDPOINT + endpoint, config);

		// Handle non-OK response
		if (!res.ok) {
			const contentType = res.headers.get('Content-Type') || '';
			const data = contentType.includes('application/json')
				? await res.json()
				: { detail: 'An error occurred' }; // Default error message for non-JSON responses

			if (res.status === 401) {
				throw redirect(303, '/account/logout');
			}
			if (res.status === 403) {
				throw error(403, data.detail || 'Forbidden');
			}

			return { error: data.detail, response: res, status: res.status };
		}

		const data = await res.json(); // Assuming API always returns JSON when successful
		return { data, response: res, status: res.status, headers: res.headers };
		// eslint-disable-next-line @typescript-eslint/no-explicit-any
	} catch (err: any) {
		console.error('API Fetch Error:', err);
		if (isRedirect(err)) {
			return redirect(303, err.location);
		}
		return {
			error: err.body?.message || 'Service Unavailable',
			status: err.status || 503,
			data: undefined
		};
	}
}

export async function apiFetchFile(
	event: RequestEvent,
	fileEndpoint: string,
	apiEndpoint: string = API_ENDPOINT
): Promise<Response> {
	const headers: Record<string, string> = {
		Authorization: `Bearer ${event.cookies.get(ACCESS_TOKEN_COOKIE_NAME)}`
	};

	const range = event.request.headers.get('range');
	if (range) headers['range'] = range;

	const response = await event.fetch(`${apiEndpoint}${fileEndpoint}`, {
		headers
	});

	if (!response.ok) {
		throw error(response.status, 'Failed to fetch file');
	}

	const newHeaders = new Headers(response.headers);

	newHeaders.delete('content-encoding');
	newHeaders.delete('content-length'); // กัน mismatch ด้วย

	return new Response(response.body, {
		status: response.status,
		headers: newHeaders
	});
}

export async function apiFetchPaginated<T>(
	event: RequestEvent,
	endpoint: string,
	queryParams: Record<string, string | number | boolean | null> = {},
	requestInit: RequestInit = {}
): Promise<FetchResponse<IPaginate<T>>> {
	const page = event.url.searchParams.get('page');
	const size = event.url.searchParams.get('size') || DEFAULT_PAGE_SIZE;
	const queryString = objectToQueryString({
		...queryParams,
		page: page,
		size: size
	});
	const targetEndpoint = `${endpoint}${queryString ? `?${queryString}` : ''}`;
	return apiFetch<IPaginate<T>>(event, targetEndpoint, requestInit);
}