<script lang="ts">
  import { PUBLIC_API_URL } from "./../../../../../../../../../../user-frontend/.svelte-kit/ambient.d.ts";
  import { superForm } from "sveltekit-superforms";
  import type { PageData } from "./$types";
  import { checkReceiptSchema } from "../check-receipt/schema";
  import { zodClient } from "sveltekit-superforms/adapters";
  import TextInput from "$lib/components/ui/forms/TextInput.svelte";
  import { toast } from "svelte-sonner";
  import { page } from "$app/state";
  import { goto } from "$app/navigation";
  import { env } from "$env/dynamic/public";

  let {
    data,
    order,
    showChangeReceiptStatusModal = $bindable(),
  }: {
    data?: PageData;
    order: any;
    showChangeReceiptStatusModal: boolean;
  } = $props();

  function formatDateTime(dateString: string) {
    const date = new Date(dateString);
    return date.toLocaleString("en-US", {
      weekday: "short",
      year: "numeric",
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
      hour12: false,
    });
  }

  const form = superForm(
    data?.form ?? {
      order_id: "",
      action: "",
    },
    {
      validators: zodClient(checkReceiptSchema),
      onResult: ({ result }) => {
        if (result.type === "success") {
          showChangeReceiptStatusModal = false;
          toast.success(`change receipt status successfully`);
          goto(page.url.pathname, { invalidateAll: true });
        } else if (result.type === "error") {
          toast.error(`Unexpected error occurred`);
          console.error(result.error);
        }
      },
      dataType: "json",
    }
  );

  const { form: formData, allErrors, enhance } = form;

  $formData.order_id = order.id;
</script>

{#if showChangeReceiptStatusModal}
  <div class="modal modal-open">
    <div class="modal-box overflow-visible bg-base-100 text-primary p-6">
      <button
        class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2"
        onclick={() => (showChangeReceiptStatusModal = false)}>✕</button
      >
      <h1 class="text-xl font-semibold mb-4">Change Receipt Status</h1>

      <!-- total-amout and create-date -->
      <h2>
        <span class="text-gray-600 min-w-[120px]">Total amount:</span>
        <span class="font-semibold">{order.total_amount}</span>
      </h2>
      <h2>
        <span class="text-gray-600 min-w-[120px]">Created at:</span>
        <span class="font-semibold">{formatDateTime(order.created_date)}</span>
      </h2>

      <!-- slip image -->
      <div class="flex flex-col items-center mt-4">
        <img
          src={`${env.PUBLIC_API_URL}/v1/orders/slip-image/${order.slip_info.file_id}`}
          alt="Receipt"
          class="w-full max-w-[400px] rounded-lg shadow-lg"
        />
      </div>

      <!-- button aprove and disapprove -->
      <div class="flex mt-4">
        <form
          method="POST"
          use:enhance
          class="w-full"
          action="orders/edit-check-receipt"
        >
          <div class="flex justify-center items-center">
            <h2 class="text-gray-600 whitespace-nowrap">
              Change order's status:
            </h2>
            <select
              name="action"
              class="select select-bordered max-w-xs ml-4"
              bind:value={$formData.action}
            >
              <option selected disabled value="">Select an action</option>
              <option value="approve">Approve</option>
              <option value="disapprove">Disapprove</option>
            </select>
          </div>

          <div class="flex justify-center">
            <button
              type="submit"
              class="btn btn-secondary btn-sm w-32 mt-4"
              name="action"
            >
              Save
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
{/if}
