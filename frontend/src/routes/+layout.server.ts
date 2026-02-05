import type { LayoutServerLoad } from "./$types";

export const load: LayoutServerLoad = async ({ locals, params }) => {
    return {
      user: locals.user ?? null,
    };
};
