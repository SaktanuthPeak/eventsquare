<script lang="ts">
  import { PencilSimpleLine } from "phosphor-svelte";
  import { createEventDispatcher } from "svelte";

  type Organization = {
    id: string;
    _id: string;
    name: string;
    role: string;
    total_event?: number;
    maximum_event?: number;
    OrganizationPic?: string;
  };

  let { organizations = [], roleFilter = "", showEditButton = true } = $props();

  const filteredOrganizations = $derived(
    roleFilter
      ? organizations.filter((org) => org.role === roleFilter)
      : organizations
  );
</script>

{#if organizations.length > 0}
  <div class="text-sm font-medium flex">
    <span class="font-medium">You are in:</span>
    <span class="badge badge-primary badge-sm ml-2">
      {filteredOrganizations.length} organization(s)
    </span>
  </div>
{/if}

{#if filteredOrganizations.length > 0}
  <div
    class="flex flex-nowrap overflow-x-auto gap-4 pb-4 w-full mt-4 scroll-smooth touch-pan-x"
  >
    {#each filteredOrganizations as org}
      <div
        class="card bg-base-100 shadow-sm w-[250px] flex-shrink-0 snap-start scroll-ml-0.5"
      >
        <figure>
          {#if org?.OrganizationPic}
            <img
              src={org.OrganizationPic}
              alt="Organization"
              class="h-36 w-full object-cover"
            />
          {:else}
            <div
              class="h-36 object-cover w-full bg-neutral-200 flex items-center justify-center"
            >
              <span
                class="text-neutral-600 font-medium cursor-default select-none"
              >
                No organization image</span
              >
            </div>
          {/if}
        </figure>
        <div class="card-body justify-items-start">
          <h2
            class="card-title text-start line-clamp-1 text-md font-semibold w-full"
          >
            {org.name}
          </h2>

          {#if org.role === "manager" || "co_manager"}
            <div class="text-sm flex">
              <span class="font-medium">Owner:</span>
              <span class="badge badge-primary badge-sm ml-2">You</span>
            </div>
          {:else}
            <div class="text-sm flex">
              <span class="font-medium">Role:</span>
              <span class="badge badge-secondary badge-sm ml-1">
                {org.role || "Staff"}
              </span>
            </div>
          {/if}

          {#if org?.total_event !== undefined}
            <span class="text-sm font-medium flex">
              Events: {org.total_event}
            </span>
          {:else if org.maximum_event}
            <span class="text-sm flex">
              Max events: {org.maximum_event}
            </span>
          {/if}

          <div class="card-actions mt-2 flex flex-row justify-between w-full">
            {#if org.role === "manager" || org.role === "co_manager"}
              <!-- ถ้าเป็น manager หรือ co-manager ให้ลิงก์ไปที่ owner -->
              <a
                href={`/manager/${org.id || org._id}/owner/view-events`}
                class="btn btn-sm btn-accent w-full"
              >
                View Details
              </a>
            {:else}
              <!-- สำหรับ staff ให้ลิงก์ไปที่ staff dashboard -->
              <a
                href={`/manager/${org.id || org._id}/staff`}
                class="btn btn-sm btn-accent w-full"
              >
                View Details
              </a>
            {/if}
          </div>
        </div>
      </div>
    {/each}
  </div>
{:else}
  <div class="text-center py-8">
    <p>
      {#if roleFilter === "manager"}
        No organizations found. Create your first organization.
      {:else}
        You are not {roleFilter} of any organization.
      {/if}
    </p>
  </div>
{/if}
