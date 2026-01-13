<script lang="ts">
  import { onMount } from "svelte";
  import type { PageData } from "./$types";
  import OrganizerOwnerNav from "../organizerOwnerNav/+page.svelte";
  import { Trash, MagnifyingGlass } from "phosphor-svelte";
  import { deleteStaffByOrganizerAndStaffId } from "$lib/client";
  import { toast } from "svelte-sonner";
  import { goto } from "$app/navigation";
  import AddStaffModal from "./add-staff/+page.svelte";

  let { data }: { data: PageData } = $props();

  // Staff data state
  let staffList = $derived(data.staff);
  let searchQuery = $state("");
  let isLoading = $state(false);
  let showAddStaffModal = $state(false);

  let currentPage = $derived(data.pagination.currentPage);
  let totalPages = $derived(data.pagination.totalPages);
  let itemsPerPage = $derived(data.pagination.itemsPerPage);

  function loadPage(pageNum: number, search: string = searchQuery) {
    isLoading = true;
    url.searchParams.set("page", pageNum.toString());
    url.searchParams.set("size", itemsPerPage.toString());
    url.searchParams.set("size", itemsPerPage.toString());

    if (search) {
      url.searchParams.set("search", search);
    } else {
      url.searchParams.delete("search");
    }

    goto(url.toString(), { keepFocus: true }).finally(() => {
      isLoading = false;
    });
  }

  function handleSearch() {
    loadPage(1, searchQuery);
  }

  async function deleteStaff(staffId: string) {
    if (confirm("Are you sure you want to remove this staff member?")) {
      try {
        await deleteStaffByOrganizerAndStaffId({
          path: {
            organizer_id: data.organization_id,
            staff_id: staffId,
          },
        });

        toast.success("Staff member removed successfully");
        loadPage(currentPage);
      } catch (error) {
        console.error("Error deleting staff:", error);
        toast.error("Failed to remove staff member");
      }
    }
  }
</script>

<OrganizerOwnerNav orgNavData={data} />
<div
  class="overflow-x-auto border-base-content/5 bg-base-100 max-w-screen px-[170px]"
>
  <div class="flex justify-between items-center mb-4 py-[5px]">
    <h1 class="text-3xl font-extrabold text-start">Organization's Staffs</h1>

    <!-- Search and Add Staff -->
    <div class="flex gap-2 items-center">
      <div class="relative p-[8px]">
        <input
          type="text"
          bind:value={searchQuery}
          placeholder="Search staff name"
          class="input focus:border-0 h-[35px] w-full max-w-xs pr-10"
          onkeydown={(e) => e.key === "Enter" && handleSearch()}
        />
        <button
          class="absolute right-3 top-1/2 transform -translate-y-1/2"
          onclick={handleSearch}
        >
          <MagnifyingGlass size={20} class="text-gray-400" />
        </button>
      </div>
      <button
        class="btn btn-primary"
        onclick={() => (showAddStaffModal = true)}
      >
        + Add Staff
      </button>
    </div>
  </div>

  <!-- Staff table -->
  <div class="overflow-x-auto rounded-lg border border-base-300">
    <table class="table w-full">
      <!-- Table head stays the same -->
      <thead class="bg-base-200">
        <tr>
          <th class="w-[5%]">Id</th>
          <th class="w-[30%]">Staff Name</th>
          <th class="w-[20%]">Username</th>
          <th class="w-[35%]">Add Date</th>
          <th class="w-[10%] text-center">Delete</th>
        </tr>
      </thead>
      <tbody>
        {#if isLoading}
          <tr>
            <td colspan="5" class="text-center py-8">Loading staff data...</td>
          </tr>
        {:else if staffList.length === 0}
          <tr>
            <td colspan="5" class="text-center py-8">No staff members found</td>
          </tr>
        {:else}
          {#each staffList as staff, index}
            <tr class="hover:bg-base-200">
              <td>{(currentPage - 1) * itemsPerPage + index + 1}</td>
              <td>
                {staff.first_name || ""}
                {staff.last_name || ""}
              </td>
              <td>{staff.username || ""}</td>
              <td>
                {staff.last_login_date}
              </td>
              <td class="text-center">
                <button
                  class="btn btn-sm btn-error btn-square"
                  onclick={() => deleteStaff(staff.id || staff._id)}
                  aria-label="Delete staff"
                >
                  <Trash size={18} weight="bold" />
                </button>
              </td>
            </tr>
          {/each}
        {/if}
      </tbody>
    </table>
  </div>

  <!-- Pagination -->
  {#if totalPages > 1}
    <div class="flex justify-center mt-4">
      <div class="join">
        <button
          class="join-item btn"
          disabled={currentPage === 1}
          onclick={() => loadPage(currentPage - 1)}
        >
          &laquo;
        </button>

        {#each Array(totalPages) as _, i}
          <button
            class="join-item btn {currentPage === i + 1 ? 'btn-primary' : ''}"
            onclick={() => loadPage(i + 1)}
          >
            {i + 1}
          </button>
        {/each}

        <button
          class="join-item btn"
          disabled={currentPage === totalPages}
          onclick={() => loadPage(currentPage + 1)}
        >
          &raquo;
        </button>
      </div>
    </div>
  {/if}
</div>

<AddStaffModal bind:showAddStaffModal {data} />
