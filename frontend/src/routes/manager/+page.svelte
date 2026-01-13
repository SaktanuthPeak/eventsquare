<script lang="ts">
  import CreateOrgModal from "./create-organizer/+page.svelte";
  import type { PageData } from "./$types";
  import OrganizationCardList from "$lib/components/cards/OrganizationCardList.svelte";

  let showCreateOrgModal = $state(false);

  type Props = { data?: PageData; organizerId?: string };

  let { data, organizerId = $bindable() }: Props = $props();
</script>

<main>
  <div class="flex flex-col text-center justify-center my-[50px] px-[200px]">
    <div class="flex flex-col gap-[15px]">
      <div class="flex justify-between items-center">
        <h1 class="font-extrabold text-3xl">Manage my Role</h1>
      </div>
      <hr />
      <div class="px-[5px]">
        <div class="items-start my-2 p-0 w-fit">
          <div class="py-[10px]">
            <h2 class="text-2xl font-extrabold">Manager</h2>
          </div>
        </div>
        <div class="card bg-base-100 shadow-md">
          <div class="card-body">
            <div class="flex justify-between items-center">
              <h2 class="card-title text-2xl font-semibold">
                Your Organization
              </h2>
              <button
                onclick={() => (showCreateOrgModal = true)}
                class="btn btn-sm btn-secondary"
              >
                Create Organization
              </button>
            </div>

            <OrganizationCardList
              organizations={data?.Organization || []}
              roleFilter="manager"
            />
          </div>
        </div>
      </div>
    </div>
    <hr class="my-[25px]" />
    <div class="px-[10px]">
      <div class="flex justify-between items-center">
        <h2 class="font-bold text-xl">Staff</h2>
      </div>
      <div class="card bg-base-100 shadow-md">
        <div class="card-body">
          <div class="flex justify-between items-center">
            <h2 class="card-title text-lg font-semibold">
              Organization you are in
            </h2>
          </div>

          <OrganizationCardList
            organizations={data?.Organization || []}
            roleFilter="staff"
            showEditButton={false}
          />
        </div>
      </div>
    </div>

    <CreateOrgModal bind:showCreateOrgModal />
  </div>
</main>
