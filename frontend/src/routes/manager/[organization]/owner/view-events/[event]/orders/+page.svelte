<script lang="ts">
  import TextInput from "$lib/components/ui/forms/TextInput.svelte";
  import { string } from "zod";
  import type { PageData } from "./$types";
  import CheckReceipteModal from "./check-receipt/+page.svelte";
  import ChangeReceiptStatusModal from "./edit-check-receipt/+page.svelte";
  import MoreInfoModal from "./more-info/+page.svelte";
  import Pagination from "$lib/components/ui/Pagination.svelte";
  import { page } from "$app/state";
  import { goto } from "$app/navigation";
  import { MagnifyingGlass } from "phosphor-svelte";
  import { get } from "svelte/store";

  let { data }: { data: PageData } = $props();
  let showCheckReceiptModal = $state(false);
  let showChangeReceiptStatusModal = $state(false);
  let showMoreInfoModal = $state(false);
  let selectedOrder = $state(null);
  let isLoading = $state(false);
  let searchQuery = $state("");
  let searchTimeout: number;

  function handleCheckReceipt(order: any) {
    selectedOrder = order;
    if (order.order_status === "pending" || order.order_status === "not_paid") {
      showCheckReceiptModal = true;
    } else {
      showChangeReceiptStatusModal = true;
    }
  }

  function handleMoreInfo(order: any) {
    selectedOrder = order;
    showMoreInfoModal = true;
  }

  function getOrderStatusBadgeClass(status: string) {
    switch (status) {
      case "completed":
        return "badge badge-success";
      case "pending":
        return "badge badge-warning";
      case "not_paid":
        return "badge badge-dash badge-error";
      case "cancelled":
        return "badge badge-error";
      default:
        return "badge-neutral";
    }
  }

  function formatDateTime(dateString: Date) {
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

  function loadPage(pageNum: number, search: string = searchQuery) {
    isLoading = true;
    const url = new URL(page.url);
    url.searchParams.set("page", pageNum.toString());

    if (search) {
      url.searchParams.set("search", search);
    } else {
      url.searchParams.delete("search");
    }

    goto(url.toString(), { keepFocus: true }).finally(() => {
      isLoading = false;
    });
  }

  function handleSearch() {
    loadPage(1, searchQuery);
  }

  function debouncedSearch(value: string) {
    if (searchTimeout) {
      clearTimeout(searchTimeout);
    }

    searchTimeout = setTimeout(() => {
      loadPage(1, value);
    }, 500);
  }
</script>

<div class="overflow-x-auto bg-base-100 max-w-screen p-4">
  <div class="flex justify-between items-center mb-6">
    <div class="flex items-center h-full">
      <h2 class="text-2xl font-bold">Orders Management</h2>
    </div>
    <div class="relative p-[8px] w-full sm:w-auto">
      <input
        type="text"
        bind:value={searchQuery}
        placeholder="Search ticket name"
        class="input focus:border-0 h-[35px] w-full max-w-xs pr-10"
        oninput={() => debouncedSearch(searchQuery)}
        onkeydown={(e) => e.key === "Enter" && handleSearch()}
      />
      <button
        class="absolute right-[20px] top-[50%] transform -translate-y-1/2"
        onclick={handleSearch}
      >
        <MagnifyingGlass size={20} class="text-gray-400" />
      </button>
    </div>
  </div>

  <div class="flex flex-col gap-4">
    {#each data.orders ?? [] as order}
      <div class="card bg-base-100 shadow-lg">
        <div class="card-body p-6">
          <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
            <!-- Left Column -->
            <div class="space-y-4">
              <div class="flex">
                <span class="text-gray-600 min-w-[120px]">Order-id:</span>
                <span class="font-semibold">{order.order_number}</span>
              </div>
              <div class="flex">
                <span class="text-gray-600 min-w-[120px]">Ticket-name:</span>
                <span class="font-semibold">{order.ticket_type_name}</span>
              </div>
              <div class="flex">
                <span class="text-gray-600 min-w-[120px]">Total amount:</span>
                <span class="font-semibold">{order.total_amount}</span>
              </div>
            </div>

            <!-- Middle Column -->
            <div class="space-y-4">
              <div class="flex mt-[37px]">
                <span class="text-gray-600 min-w-[120px]">Ticket Qty:</span>
                <span class="font-semibold">{order.audience_per_ticket}</span>
              </div>
              <div class="flex">
                <span class="text-gray-600 min-w-[120px]">Order Created:</span>
                <span class="font-semibold"
                  >{formatDateTime(order.created_date)}</span
                >
              </div>
            </div>

            <!-- Right Column -->
            <div class="space-y-4 flex flex-col items-end">
              <div class={getOrderStatusBadgeClass(order?.order_status || "")}>
                {order.order_status}
              </div>

              <button
                class="btn btn-primary btn-sm w-32"
                onclick={() => handleCheckReceipt(order)}>Check Receipt</button
              >
              <button
                class="w-32 underline cursor-pointer"
                onclick={() => handleMoreInfo(order)}>more info</button
              >
            </div>
          </div>
        </div>
      </div>
    {/each}

    <Pagination
      pagination={data?.pagination}
      onPageChange={(pageNum: any) => loadPage(pageNum, searchQuery)}
      size="sm"
    />
  </div>
</div>

{#if showCheckReceiptModal}
  <CheckReceipteModal bind:showCheckReceiptModal order={selectedOrder} />
{/if}

{#if showChangeReceiptStatusModal}
  <ChangeReceiptStatusModal
    bind:showChangeReceiptStatusModal
    order={selectedOrder}
  />
{/if}

{#if showMoreInfoModal}
  <MoreInfoModal bind:showMoreInfoModal order={selectedOrder} />
{/if}
