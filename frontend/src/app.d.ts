// See https://svelte.dev/docs/kit/types#app.d.ts

import type { Client } from '@hey-api/client-fetch';
import type { IBackOfficeUser } from '$lib/models/back-office-users';

// for information about these interfaces
declare global {
	namespace App {
		// interface Error {}
		// interface Locals {}
		// interface PageData {}
		// interface PageState {}
		// interface Platform {}
		interface Locals {
				client?: Client;

				user?: {
					id: string;
					username: string;
					first_name: string;
					last_name: string;
					roles: string[];
				};
				token?: string;

				back_office_user?: IBackOfficeUser;
				back_office_token?: string;

		}
	}
}

export { };