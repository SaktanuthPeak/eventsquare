<script lang="ts">
  import { CaretRight, CaretDown } from "phosphor-svelte";
  import type { PageData } from "./$types";
  import { cn } from "$lib/utils/tw-utils";

  let { data }: { data: PageData } = $props();

  let organizationId = $state(data?.organization_id);
  let eventId = $state(data?.event_id);
  function getEventStatusClass(status: string) {
    switch (status) {
      case "active":
        return "text-green-500";
      case "inactive":
        return "text-red-500";
      case "draft":
        return "text-yellow-500";
      case "cancelled":
        return "text-red-500";
      case "completed":
        return "text-gray-500";
      case "archived":
        return "text-gray-500";
      default:
        return "text-gray-500";
    }
  }
</script>

<nav class="navbar event-navbar">
  <div class="flex flex-col gap-[10px] w-full">
    <div class="w-full flex flex-col border-b-[1.7px] border-base-content/25">
      <div class="w-full flex flex-row justify-between items-center">
        <div class="flex flex-col gap-[10px]">
          {#if data?.eventData?.title}
            <p class="font-bold text-xl">{data?.eventData?.title}</p>
          {:else}
            <p class="font-bold text-xl">Event Title</p>
          {/if}
          <p class="font-medium text-md">
            Event Status:
            <span
              class={cn(getEventStatusClass(data?.eventData?.event_status))}
            >
              {data?.eventData?.event_status
                ? data?.eventData?.event_status.charAt(0).toUpperCase() +
                  data?.eventData?.event_status.slice(1)
                : "Unknown"}
            </span>
          </p>
        </div>
        <a
          class="btn btn-secondary w-[150px] h-[32px]"
          href="/manager/{organizationId}/owner/view-events/{eventId}/upload-img"
          >Edit Design</a
        >
      </div>
      <div class="w-full flex flex-row items-center mt-[10px]">
        <a
          class="flex py-[8px] self-center justify-center w-[130px] text-[#676D75] font-medium text-[16px]
     hover:text-primary"
          href="/manager/{organizationId}/owner/view-events">All Events</a
        >
        <CaretRight size={16} class="mx-1 text-[#676D75]" />

        <!-- Overview -->
        <a
          class="event-navbar-event-ctrl-btn"
          href="/manager/{organizationId}/owner/view-events/{eventId}/overview"
          ><p class="line-clamp-1">Overview</p></a
        >

        <!-- Event Details -->
        <a
          class="event-navbar-event-ctrl-btn"
          href="/manager/{organizationId}/owner/view-events/{eventId}/event-details"
        >
          <p class="line-clamp-1">Event Details</p></a
        >

        <!-- Ticket Details -->
        <div class="event-navbar-event-ctrl-btn">
          <div id="ticket-details" class="dropdown dropdown-center">
            <div tabIndex={0} role="button" class="flex flex-row items-center">
              <p class="line-clamp-1">Ticket Details</p>
              <CaretDown size={16} class="mx-1" />
            </div>
            <ul
              tabIndex={0}
              class="dropdown-content menu shadow bg-base-100 rounded-b-sm gap-1 w-[150px]"
            >
              <li>
                <a
                  class="rounded-lg hover:bg-gray-100 hover:shadow-[0_2px_0_0_currentColor]"
                  href="/manager/{organizationId}/owner/view-events/{eventId}/tickets-type"
                  >Tickets type</a
                >
              </li>
              <li>
                <a
                  class="rounded-lg hover:bg-gray-100 hover:shadow-[0_2px_0_0_currentColor]"
                  href="/manager/{organizationId}/owner/view-events/{eventId}/hard-tickets"
                  >Hard-Tickets</a
                >
              </li>
            </ul>
          </div>
        </div>

        <!-- Manage Staffs -->
        <a
          class="event-navbar-event-ctrl-btn"
          href="/manager/{organizationId}/owner/view-events/{eventId}/staffs"
          ><p class="line-clamp-1">Staffs</p></a
        >

        <!-- Scan log -->
        <a
          class="event-navbar-event-ctrl-btn"
          href="/manager/{organizationId}/owner/view-events/{eventId}/scan-log"
          ><p class="line-clamp-1">Scan log</p></a
        >

        <!-- Order -->
        <a
          class="event-navbar-event-ctrl-btn"
          href="/manager/{organizationId}/owner/view-events/{eventId}/orders"
          ><p class="line-clamp-1">Orders</p></a
        >
      </div>
    </div>
  </div>
</nav>
