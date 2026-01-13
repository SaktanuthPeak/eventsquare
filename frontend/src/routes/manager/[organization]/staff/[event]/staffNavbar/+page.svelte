<script lang="ts">
  import { CaretRight, CaretDown } from "phosphor-svelte";
  import type { PageData } from "./$types";
  import { cn } from "$lib/utils/tw-utils";

  let { data }: { data: PageData } = $props();

  let organizationId = $state(data?.organization_id);
  let eventId = $state(data?.event_id);
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
              class={cn(
                data?.eventData?.event_status === "active" && "text-green-500",
                data?.eventData?.event_status === "inactive" && "text-red-500",
                data?.eventData?.event_status === "draft" && "text-yellow-500",
                data?.eventData?.event_status === "cancelled" && "text-red-500",
                data?.eventData?.event_status === "completed" &&
                  "text-gray-500",
                data?.eventData?.event_status === "archived" && "text-gray-500",
                !data?.eventData?.event_status && "text-gray-500"
              )}
            >
              {data?.eventData?.event_status
                ? data?.eventData?.event_status.charAt(0).toUpperCase() +
                  data?.eventData?.event_status.slice(1)
                : "Unknown"}
            </span>
          </p>
        </div>
      </div>
      <div class="w-full flex flex-row items-center mt-[10px]">
        <!-- Overview -->
        <a
          class="event-navbar-event-ctrl-btn"
          href="/manager/{organizationId}/staff/{eventId}/scan-page"
          ><p class="line-clamp-1">Scan Page</p></a
        >

        <!-- Event Details -->
        <a
          class="event-navbar-event-ctrl-btn"
          href="/manager/{organizationId}/staff/{eventId}/ticket-buyers"
        >
          <p class="line-clamp-1">Ticket Buyers</p></a
        >
      </div>
    </div>
  </div>
</nav>
