<script lang="ts">
  import { onMount } from "svelte";
  import type { PageData } from "./$types";
  import OrganizerOwnerNav from "../organizerOwnerNav/+page.svelte";
  import { cn } from "$lib/utils/tw-utils";
  import EventCard from "$lib/components/cards/EventCard.svelte";
  import { organizeSchema } from "../../../create-organizer/schema";

  let { data }: { data: PageData } = $props();
</script>

<OrganizerOwnerNav orgNavData={data} />
<div class="min-h-screen bg-base-100 px-[200px]">
  <div class="mx-auto max-w-7xl">
    <div
      class="flex flex-row items-center justify-between mb-8 border-b-2 border-base-content/10 pb-6"
    >
      <h1 class="text-3xl font-bold text-base-content">
        Active Events
        {#if data?.events?.filter((event) => event.event_status === "active")?.length > 0}
          <span class="ml-3 text-lg font-medium text-base-content/60">
            ({data?.events?.filter((event) => event.event_status === "active")
              ?.length} ongoing)
          </span>
        {/if}
      </h1>

      <div
        class={cn(
          "flex flex-row items-center gap-4",
          data?.events?.filter((event) => event.event_status === "active")
            ?.length >= data?.organization?.organizer.maximum_event
            ? "hidden"
            : ""
        )}
      >
        <a
          href="/manager/{data.organization_id}/owner/view-events/create-event"
          class="btn btn-primary text-primary-content"
        >
          Create Event
        </a>
      </div>
    </div>

    <!-- Events Grid -->
    {#if data?.events?.filter((event) => event.event_status === "active")?.length === 0}
      <div class="flex h-96 items-center justify-center rounded-xl bg-base-100">
        <p class="text-xl font-medium text-base-content/70">
          No active events found
        </p>
      </div>
    {:else}
      <div
        class="grid grid-cols-1 gap-6 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5"
      >
        {#each data?.events?.filter((event) => event.event_status === "active") as event}
          <EventCard
            {event}
            organizationId={data.organization_id}
            userRole={data.orgUserData?.find(
              (org) => org.id === data.organization_id
            )?.role}
          />
        {/each}
      </div>
    {/if}
  </div>
</div>
