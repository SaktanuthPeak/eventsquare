<script lang="ts">
  import type { PageData } from "./$types";
  import { Eye, MagnifyingGlass, Trash } from "phosphor-svelte";
  import CreateETicketModal from "./create-tickets-type/+page.svelte";
  import DeleteTicketModal from "$lib/components/modals/DeleteTicketModal.svelte";
  import Pagination from "$lib/components/ui/Pagination.svelte";
  import { onMount, onDestroy } from "svelte";
  import { goto } from "$app/navigation";
  import { page } from "$app/stores";
  import { toast } from "svelte-sonner";
  import { enhance } from "$app/forms";

  let { data }: { data: PageData } = $props();
  let showCreateETicketModal: boolean = $state(false);
  let searchQuery = $state("");
  let isLoading = $state(false);
  let searchTimeout: number;
  let showDeleteConfirmModal = $state(false);
  let ticketToDelete = $state<{ id: string; name: string } | null>(null);

  let showAllDatesModal = $state(false);
  let selectedDates = $state([]);
  let selectedTicketName = $state("");

  function loadPage(pageNum: number, search: string = searchQuery) {
    isLoading = true;
    const url = new URL($page.url);
    url.searchParams.set("page", pageNum.toString());

    if (search) {
      url.searchParams.set("search", search);
    } else {
      url.searchParams.delete("search");
    }

    goto(url.toString(), { keepFocus: true, invalidateAll: true }).finally(
      () => {
        isLoading = false;
      }
    );
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

  function confirmDelete(ticket_type_id: string, ticket_name: string) {
    ticketToDelete = {
      id: ticket_type_id,
      name: ticket_name,
    };
    showDeleteConfirmModal = true;
  }

  function showAllDates(ticket) {
    selectedDates = ticket.allowed_dates;
    selectedTicketName = ticket.name;
    showAllDatesModal = true;
  }

  onMount(() => {
    searchQuery = $page.url.searchParams.get("search") || "";
  });

  onDestroy(() => {
    if (searchTimeout) {
      clearTimeout(searchTimeout);
    }
  });
</script>

<div class="flex flex-col items-center w-full mb-[20px]">
  <div class="flex flex-col sm:flex-row justify-between w-full gap-2">
    <h2 class="text-2xl font-bold p-4">Tickets type Details</h2>
    <div class="flex flex-col sm:flex-row gap-2 items-center">
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

      <button
        class="btn btn-primary rounded-sm text-[14px] font-bold h-[32px] m-2 sm:m-4 w-full sm:w-auto"
        onclick={() => (showCreateETicketModal = true)}
      >
        + Add Ticket
      </button>
    </div>
  </div>

  <!-- Responsive table container -->
  <div
    class="w-full overflow-x-auto rounded-box border border-base-content/5 bg-base-100"
  >
    <div class="min-w-[900px]">
      <!-- Minimum width to ensure table is readable -->
      <table class="table w-full">
        <thead class="font-medium text-base-content bg-gray-200">
          <tr class="">
            <th class="w-[5%] hidden sm:table-cell">Id</th>
            <th class="w-[17%]">Ticket Name</th>
            <th class="w-[10%]">Price</th>
            <th class="w-[10%] hidden sm:table-cell">Qty.</th>
            <th class="w-[33%] hidden md:table-cell">Entry Period</th>
            <th class="w-[10%] hidden lg:table-cell text-center">Remaining</th>
            <th class="w-[10%] text-center">Status</th>
            <th class="w-[5%] text-center">
              <span class="hidden sm:inline">Delete</span>
              <span class="sm:hidden">🗑️</span>
            </th>
            <th class="w-[5%] text-center">
              <span class="hidden sm:inline">View</span>
              <span class="sm:hidden">👁️</span>
            </th>
          </tr>
        </thead>
        <tbody>
          {#if isLoading}
            <tr>
              <td colspan="9" class="text-center py-4">
                <div class="loading loading-spinner loading-md"></div>
              </td>
            </tr>
          {:else if !data?.eventData?.ticket_types || data.eventData.ticket_types.length === 0}
            <tr>
              <td colspan="9" class="text-center">
                <p class="text-base-content/70">No tickets found</p>
              </td>
            </tr>
          {:else}
            {#each data.eventData.ticket_types as ticket, index}
              <tr class="hover:bg-base-200 border-t border-base-300">
                <td class="hidden sm:table-cell">
                  {(data.pagination.currentPage - 1) *
                    data.pagination.itemsPerPage +
                    index +
                    1}
                </td>
                <td>
                  <p class="font-medium line-clamp-1">
                    {ticket?.name || "* No title shown *"}
                  </p>
                </td>
                <td>
                  <p class="line-clamp-1">
                    {ticket?.price ? `${ticket?.price}` : "-"}
                  </p>
                </td>
                <td class="hidden sm:table-cell text-center">
                  {ticket?.audience_quantity}
                </td>
                <td class="hidden md:table-cell">
                  <div class="flex flex-col">
                    <div
                      class="flex flex-row gap-1 flex-wrap max-h-[60px] overflow-hidden"
                    >
                      {#each ticket?.allowed_dates.slice(0, 2) as date, i}
                        <div class="badge badge-primary badge-sm">
                          {new Date(date).toLocaleDateString("en-GB", {
                            day: "numeric",
                            month: "short",
                            year: "numeric",
                          })}
                        </div>
                      {/each}
                      {#if ticket?.allowed_dates.length > 2}
                        <button
                          class="badge badge-sm border-1 border-gray-700 text-gray-600 hover:bg-gray-200 cursor-pointer"
                          onclick={() => showAllDates(ticket)}
                          >+{ticket?.allowed_dates.length - 2}</button
                        >
                      {/if}
                    </div>
                  </div>
                </td>
                <td class="hidden lg:table-cell text-center">
                  {ticket?.quantity_remaining} / {ticket?.audience_quantity}
                </td>
                <td class="text-center">
                  {#if ticket?.ticket_status === "disabled"}
                    <div class="badge badge-error badge-sm">Disabled</div>
                  {:else}
                    <div class="badge badge-success badge-sm">Available</div>
                  {/if}
                </td>
                <td class="text-center">
                  <button
                    class="btn btn-sm size-8 p-0 border-0 rounded-md bg-red-500 hover:bg-red-700"
                    onclick={() => confirmDelete(ticket.id, ticket.name)}
                    aria-label="Delete ticket"
                  >
                    <Trash size={15} color="white" weight="bold" />
                  </button>
                </td>
                <td class="text-center">
                  <button
                    class="btn btn-sm size-8 p-0 border-0 rounded-md bg-gray-100 hover:bg-gray-200"
                  >
                    <Eye size={15} color="black" weight="bold" />
                  </button>
                </td>
              </tr>
            {/each}
          {/if}
        </tbody>
      </table>
    </div>
  </div>

  <div class="sm:hidden text-sm text-gray-500 mt-2 flex items-center">
    <span>← Scroll horizontally to see more →</span>
  </div>

  <Pagination
    pagination={data?.pagination}
    onPageChange={(pageNum) => loadPage(pageNum, searchQuery)}
    size="sm"
  />
</div>

<DeleteTicketModal bind:show={showDeleteConfirmModal} bind:ticketToDelete />

{#if showAllDatesModal}
  <div class="modal modal-open">
    <div class="modal-box bg-base-100 text-primary">
      <h3 class="font-bold text-lg mb-4">
        Entry Dates for "{selectedTicketName}"
      </h3>
      <div class="flex flex-wrap gap-2 max-h-[300px] overflow-y-auto p-2">
        {#each selectedDates as date}
          <div class="badge badge-lg badge-primary">
            {new Date(date).toLocaleDateString("en-US", {
              day: "numeric",
              month: "short",
              year: "numeric",
            })}
          </div>
        {/each}
      </div>
      <div class="modal-action mt-4">
        <button class="btn" onclick={() => (showAllDatesModal = false)}
          >Close</button
        >
      </div>
    </div>
    <button
      type="button"
      class="modal-backdrop"
      aria-label="Close modal"
      onclick={() => (showAllDatesModal = false)}
    ></button>
  </div>
{/if}

<CreateETicketModal
  bind:showCreateETicketModal
  organizationId={data.organization_id}
  eventId={data.event_id}
/>
