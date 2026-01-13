<script lang="ts">
  import { CaretRight, CaretDown } from "phosphor-svelte";
  import type { PageData } from "./$types";
  import { cn } from "$lib/utils/tw-utils";
  import { page } from "$app/state";
  import { onMount } from "svelte";
  import { goto } from "$app/navigation";
  import GetCheckInQr from "../get-checkin-qr/+page.svelte";
  import ShowDeleteModal from "../delete-event-modal/+page.svelte";

  let { data }: { data: PageData } = $props();
  let organizationId = $state(data?.organization_id);
  let eventId = $state(data?.event_id);
  let showGetCheckInQrModal: boolean = $state(false);
  let showDeleteEventModal: boolean = $state(false);

  const allowedPaths = ["overview", "event-details", "check-in-log"];

  const currentPath: string = page.url.pathname.split("/").pop() || "";
  onMount(() => {
    if (!allowedPaths.includes(currentPath)) {
      goto(`/manager/${organizationId}/owner/view-events/${eventId}/overview`);
    }
  });

  function getEventStatusClass(status: string) {
    switch (status) {
      case "active":
        return "badge badge-success ml-2 text-xs";
      case "inactive":
        return "badge badge-error ml-2 text-xs";
      case "draft":
        return "badge badge-neutral ml-2 text-xs";
      case "cancelled":
        return "badge badge-error ml-2 text-xs";
      case "completed":
        return "badge badge-error ml-2 text-xs";
      case "archived":
        return "badge badge-warning ml-2 text-xs";
      default:
        return "badge badge-ghost ml-2 text-xs";
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
              class={cn(
                getEventStatusClass(data?.eventData?.event_status ?? "")
              )}
            >
              {data?.eventData?.event_status
                ? data?.eventData?.event_status.charAt(0).toUpperCase() +
                  data?.eventData?.event_status.slice(1)
                : "Unknown"}
            </span>
          </p>
        </div>
        <div>
          <button
            class="btn btn-secondary w-[150px] h-[32px]"
            onclick={() => (showGetCheckInQrModal = true)}>Get Qrcode</button
          >
          <button
            class="btn btn-error w-[150px] h-[32px]"
            onclick={() => (showDeleteEventModal = true)}>Delete</button
          >
        </div>
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

        <!-- Scan log -->
        <a
          class="event-navbar-event-ctrl-btn"
          href="/manager/{organizationId}/owner/view-events/{eventId}/check-in-log"
          ><p class="line-clamp-1">Check-in log</p></a
        >
      </div>
    </div>
  </div>
</nav>
<GetCheckInQr {data} bind:showGetCheckInQrModal />

{#if showDeleteEventModal}
  <ShowDeleteModal {data} bind:showDeleteEventModal />
{/if}
