// See https://svelte.dev/docs/kit/types#app.d.ts

import type { Client } from "@hey-api/client-fetch";

// for information about these interfaces
declare global {
  namespace App {
    // interface Error {}
    // interface Locals {}
    // interface PageData {}
    // interface PageState {}
    // interface Platform {}

    interface Locals {
      user: {
        id: string;
        username: string;
        first_name: string;
        last_name: string;
        roles: string[];
      },
      client: Client
    }
  }
}

export { };
