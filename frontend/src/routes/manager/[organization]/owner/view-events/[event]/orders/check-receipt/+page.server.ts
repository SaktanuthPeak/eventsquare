import { confirmOrder, getOrdersByOrganizer, updateOrder } from "$lib/client";
import { superValidate } from "sveltekit-superforms";
import type { PageServerLoad } from "./$types";
import { zod } from "sveltekit-superforms/adapters";
import { checkReceiptSchema } from "./schema";
import { fail } from "@sveltejs/kit";

export const load: PageServerLoad = async (params) => {
  const form = await superValidate(zod(checkReceiptSchema));
  return {
    form,
  };
};

export const actions = {
  default: async ({ locals,request }) => {
    const form = await superValidate(request, zod(checkReceiptSchema));
    const { client } = locals;

    let action = form.data.action;

    if (!form.valid) {
      return fail(400, { form });
    }
    switch (action) {
      case "approve":
        try {
          const res = await confirmOrder({
            client: client,
            path: {
              order_id: form.data.order_id,
            },
          });

          if (!res.response.ok) {
            return {
              form,
            };
          }

          return {
            form,
            type: "success",
          };
        } catch (e) {
          console.log("Error approving receipt:", e);
          return {
            form,
            type: "error",
          };
        } finally {
          console.log("Finally block executed");
        }

      case "disapprove":
        try {
          const res = await updateOrder({
            client: client,
            path: {
              order_id: form.data.order_id,
            },
            body: {
              order_status: "cancelled",
            },
          });

          if (!res.response.ok) {
            return {
              form,
              type: "error",
            };
          }

          return {
            form,
            type: "success",
          };
        } catch (e) {
          console.log("Error disapproving receipt:", e);
          return {
            form,
            type: "error",
          };
        }
      default:
        console.error("Invalid action:", action);
        return fail(400, { form });
    }
  },
};
