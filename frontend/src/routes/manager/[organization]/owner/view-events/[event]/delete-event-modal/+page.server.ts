import { superValidate } from "sveltekit-superforms";
import type { PageServerLoad } from "./$types";
import { zod } from "sveltekit-superforms/adapters";
import { deleteEventSchema } from "./schema";
import { partialUpdateEventById } from "$lib/client";

export const load = (async () => {
    const form = await superValidate(zod(deleteEventSchema));
    return { form };

}) satisfies PageServerLoad;

export const actions = {
    default: async ({ request, params, locals }) => {
        const form = await superValidate(request, zod(deleteEventSchema));
        const { client } = locals;

        try{
            const res  = await partialUpdateEventById({
                client: client,
                path:{
                    event_id: form.data.eventId,
                },
                body:{
                    event_status: "deleted",
                }
            })

            if(!res.response.ok) {
                return {
                    form,
                    type: "failure",
                    message: res.error?.errors?.[0] || "Failed to delete event",
                };
            }

            return{
                form,
                type: "success",
                message: "Event deleted successfully",
            }
        }catch (error) {
            
        }
        

        return {
            success: true,
            message: "Event deleted successfully",
        };
    },
};