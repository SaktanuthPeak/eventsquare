<script lang="ts">
  import { fade } from "svelte/transition";
  import { env } from "$env/dynamic/public";
  import { cn } from "$lib/utils/tw-utils";
  import { goto } from "$app/navigation";

  let { event, organizationId, userRole = "staff" } = $props();

  let statusDisplay = $derived(
    event?.event_status
      ? event.event_status.charAt(0).toUpperCase() + event.event_status.slice(1)
      : "Unknown"
  );

  function getStatusClass(status: string) {
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

  let typeDisplay = $derived(
    event?.event_type
      ? event.event_type.charAt(0).toUpperCase() + event.event_type.slice(1)
      : "Unknown"
  );

  let detailsPath = $derived(
    userRole === "staff"
      ? `/manager/${organizationId}/staff/${event?.id}/scan-page` // Staff path
      : `/manager/${organizationId}/owner/view-events/${event?.id}/overview` // Owner/manager path
  );

  function getTypeClass(type: string) {
    switch (type) {
      case "public":
        return "badge badge-secondary ml-2 text-xs";
      case "private":
        return "badge badge-accent ml-2 text-xs";
      default:
        return "badge badge-ghost ml-2 text-xs";
    }
  }
</script>

<a
  transition:fade={{ duration: 500 }}
  href={detailsPath}
  class="card group items-center justify-center overflow-hidden bg-base-300 shadow-lg transition-all w-[180px] h-[390px] duration-300 hover:shadow-xl"
>
  <figure class="relative rounded-2xl h-[240px] w-[180px]">
    {#if event?.image}
      <img
        src={`${env.PUBLIC_API_URL}/v1/events/image/${event.image.file_id}`}
        alt={event.title}
        class="h-[240px] w-[180px] object-cover transition-transform duration-300 group-hover:scale-105"
      />
    {:else}
      <div
        class="flex h-[240px] w-[180px] items-center justify-center bg-gray transition-transform duration-300 group-hover:scale-105"
      >
        <span class="text-lg font-medium text-base-content/40 select-none">
          No Image Available
        </span>
      </div>
    {/if}
  </figure>

  <div class="card-body p-1 w-full">
    <h2
      class="card-title text-base-content text-lg line-clamp-1"
      title={event.title}
    >
      {event.title}
    </h2>
    <div class="card-title text-base-content text-sm">
      Type:
      <span class={getTypeClass(event.event_type)}>
        {typeDisplay}
      </span>
    </div>
    <div class="card-title text-base-content text-sm">
      Status:
      <span class={getStatusClass(event.event_status)}>
        {statusDisplay}
      </span>
    </div>
    <div class="card-actions flex flex-col w-full gap-1">
      <button
        onclick={() => goto(detailsPath)}
        class="btn btn-primary btn-block btn-sm text-primary-content"
      >
        View Details
      </button>
    </div>
  </div>
</a>
