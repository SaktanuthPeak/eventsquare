<script lang="ts">
  import { asClassComponent } from "svelte/legacy";
  import type { PageData } from "./$types";
  import { Download, DownloadSimple, Eye, Trash } from "phosphor-svelte";

  let { data }: { data: PageData } = $props();
</script>

<!-- todo add "Add ticket" function and handle datat to table -->

<div class="flex flex-col items-center">
  <div class="flex flex-row justify-between w-full">
    <h2 class="text-2xl font-bold text-center p-4">Hard-Tickets Details</h2>
    <a
      class="btn btn-primary rounded-sm text-[14px] font-bold h-[32px] m-4"
      href="/manager/oragnizationId/view-events/eventId/hard-tickets/create"
    >
      + Add Ticket
    </a>
  </div>
  <div
    class="overflow-x-auto rounded-box border border-base-content/5 bg-base-100 max-w-screen"
  >
    <table class="table">
      <thead class=" font-medium text-base-content bg-gray-200">
        <tr class="">
          <th class="w-[30px]">Id</th>
          <th class="w-[230px]">Ticket Name</th>
          <th class="w-[130px]">Price</th>
          <th class="w-[60px] text-center"><p>Ticket Qty.</p></th>
          <th class="w-[420px]">Entry Period</th>
          <th class="text-center w-[125px]"><p>Status</p></th>
          <th class="text-center w-[70px]">
            <p>QR</p>
          </th>
          <th class="text-center w-[70px]">
            <p>Delete</p>
          </th>
          <th class="text-center w-[70px]"><p>View</p></th>
        </tr>
      </thead>
      <tbody class="h-[32px] p-0">
        <tr class="h-[32px]">
          <td class="">1</td>
          <td><p class=" line-clamp-1">Ganderton</p> </td>
          <td><p class=" line-clamp-1">2,000</p></td>
          <td><p class="text-center line-clamp-1">50</p></td>
          <td>1</td>
          <td class="h-[32px]">
            <div class="flex h-full w-full justify-center items-center">
              <!-- {#if ticket.ticketStatus === "avaliable"} -->
              <div class="badge badge-success">Avaliable</div>
              <!-- {:else if ticket.ticketStatus === "disabled"}
            <div class="badge badge-error">Disabled</div>
            {:else }
            <div class="badge badge-warning">Pending</div>
            {/if} -->
            </div>
          </td>
          <td class="w-[70px] items-center text-center">
            <button
              class="btn btn-sm size-[30px] p-0.5 border-0 rounded-md bg-blue-500 hover:bg-blue-700"
            >
              <DownloadSimple size={16} color="white" weight="bold" />
            </button>
          </td>
          <td class="w-[70px] items-center text-center"
            ><button
              class="btn btn-sm size-[30px] p-0.5 border-0 rounded-md bg-red-500 hover:bg-red-700"
            >
              <Trash size={16} color="white" weight="bold" /></button
            ></td
          >
          <td class="w-[70px] items-center text-center"
            ><button
              class="btn btn-sm size-[30px] p-0.5 border-2 rounded-md hover:bg-black/15"
            >
              <Eye size={16} color="black" weight="bold" /></button
            ></td
          >
        </tr>
      </tbody>
    </table>
  </div>
</div>
