<script lang="ts">
  import EventCard from "$lib/components/cards/EventCard.svelte";
  import type { PageData } from "./$types";

  let { data }: { data: PageData } = $props();
</script>

<main>
  <div class="flex flex-col min-h-screen">
    <div class="mt-[50px] px-[200px]">
      <h1 class="text-2xl font-bold">
        Events in " <span class="text-accent font-bold">
          {data?.orgData?.organizer?.name}
        </span> " Organization
      </h1>
      <p class="text-lg"></p>
    </div>

    <div class="mt-[20px] px-[200px]">
      {#if data?.events?.filter((event) => event.event_status === "active")?.length === 0}
        <div
          class="flex h-96 items-center justify-center rounded-xl bg-base-100"
        >
          <p class="text-xl font-medium text-base-content/70">
            No active events found
          </p>
        </div>
      {:else}
        <div
          class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4"
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
</main>
