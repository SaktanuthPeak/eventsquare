<script lang="ts">
  import type { PageData } from "./$types";

  let {
    order,
    showMoreInfoModal = $bindable(),
  }: {
    data?: PageData;
    order: any;
    showMoreInfoModal: boolean;
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
</script>

{#if showMoreInfoModal}
  <div class="modal modal-open">
    <div class="modal-box overflow-visible bg-base-100 text-primary p-6">
      <button
        class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2"
        onclick={() => (showMoreInfoModal = false)}>✕</button
      >
      <div class="flex items-center">
        <h1 class="text-2xl font-semibold">Order info</h1>
        <span class="text-gray-600 min-w-[120px] ml-2"
          >id: {order.order_number}</span
        >
      </div>

      <div class="space-y-4 mt-4">
        <!-- owner/co-owner name -->
        <div class="flex">
          <span class="text-gray-600 min-w-[150px]">Owner Name:</span>
          <span class="font-semibold">{order.owner_name}</span>
        </div>
        <div class="flex">
          <span class="text-gray-600 min-w-[150px]">Co-Owner Name:</span>
          <span class="font-semibold"
            >{order.co_owner_name ? order.co_owner_name : "No data"}</span
          >
        </div>

        <!-- owner/co-owner gmail -->
        <div class="flex">
          <span class="text-gray-600 min-w-[150px]">Owner Gmail:</span>
          <span class="font-semibold">{formatDateTime(order.owner_email)}</span>
        </div>
        <div class="flex">
          <span class="text-gray-600 min-w-[150px]">Co-Owner Gmail:</span>
          <span class="font-semibold"
            >{order.co_owner_gmail ? order.co_owner_gmail : "No data"}</span
          >
        </div>

        <!-- owner/co-owner gmail -->
        <div class="flex">
          <span class="text-gray-600 min-w-[150px]">Owner Phone:</span>
          <span class="font-semibold">{order.owner_phone}</span>
        </div>
        <div class="flex">
          <span class="text-gray-600 min-w-[150px]">Co-Owner Phone:</span>
          <span class="font-semibold"
            >{order.co_owner_phone ? order.co_owner_phone : "No data"}</span
          >
        </div>

        <!-- order info -->
        <div class="flex">
          <span class="text-gray-600 min-w-[150px]">Ticket name:</span>
          <span class="font-semibold">{order.ticket_type_name}</span>
        </div>
        <div class="flex">
          <span class="text-gray-600 min-w-[150px]">Audince:</span>
          <span class="font-semibold">{order.audience_per_ticket}</span>
        </div>
        <div class="flex">
          <span class="text-gray-600 min-w-[150px]">Total amount:</span>
          <span class="font-semibold">{order.total_amount}</span>
        </div>
        <div class="flex">
          <span class="text-gray-600 min-w-[150px]">Created at:</span>
          <span class="font-semibold">{formatDateTime(order.created_date)}</span
          >
        </div>
      </div>
    </div>
  </div>
{/if}
