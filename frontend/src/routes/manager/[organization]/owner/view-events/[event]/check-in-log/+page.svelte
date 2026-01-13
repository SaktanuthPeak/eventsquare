<script lang="ts">
  import DatePicker from "$lib/components/ui/forms/DatePicker.svelte";
  import { MagnifyingGlass } from "phosphor-svelte";
  import type { PageData } from "./$types";
  import { goto } from "$app/navigation";
  import { page } from "$app/state";
  import Pagination from "$lib/components/ui/Pagination.svelte";
  import { formatDateTime } from "$lib/utils/date-utils";

  let { data }: { data: PageData } = $props();

  let isLoading = $state(false);
  let searchQuery = $state("");
  let dateQuery = $state("");
  let searchTimeout: number;

  function loadPage(
    pageNum: number,
    search: string = searchQuery,
    date: string = dateQuery
  ) {
    isLoading = true;
    const url = new URL(page.url);
    url.searchParams.set("page", pageNum.toString());

    if (search) {
      url.searchParams.set("search", search);
    } else {
      url.searchParams.delete("search");
    }

    if (date) {
      url.searchParams.set("date", date);
    } else {
      url.searchParams.delete("date");
    }

    goto(url.toString(), { keepFocus: true }).finally(() => {
      isLoading = false;
    });
  }

  function handleSearch() {
    if (searchQuery && dateQuery) {
      loadPage(1, searchQuery, dateQuery);
    } else if (searchQuery) {
      loadPage(1, searchQuery);
    } else {
      loadPage(1, dateQuery);
    }
  }

  function debouncedSearch(value: string) {
    if (searchTimeout) clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => loadPage(1, value, dateQuery), 500);
  }

  function debouncedDateSearch(value: string) {
    if (searchTimeout) clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => loadPage(1, searchQuery, value), 500);
  }

  $effect(() => {
    debouncedDateSearch(dateQuery);
  });
</script>

<div>
  <div class="flex justify-between items-center">
    <div class="flex items-end gap-2">
      <h2 class="text-2xl font-bold pt-5 pb-1">Check-in log</h2>
      <p class="text-base-content/70 text-start pb-2">
        (Total Participants: {data.pagination.totalItems})
      </p>
    </div>
    <div class="flex items-center gap-1">
      <div class="relative p-[8px] w-full sm:w-auto">
        <DatePicker
          bind:value={dateQuery}
          placeholder="Search Date"
          class="input focus:border-0 h-[35px] w-full max-w-xs pr-10"
        />
      </div>
      <div class="relative p-[8px] w-full sm:w-auto">
        <input
          type="text"
          bind:value={searchQuery}
          placeholder="Search Name"
          class="input focus:border-0 h-[35px] w-full max-w-xs pr-10"
          oninput={() => debouncedSearch(searchQuery)}
          onkeydown={(e) => e.key === "Enter" && handleSearch()}
        />
        <button
          class="absolute right-[20px] top-[50%] transform -translate-y-1/2"
          onclick={handleSearch}
        >
          <MagnifyingGlass size={20} class="text-gray-400" />
        </button>
      </div>
    </div>
  </div>
  <div
    class="w-full overflow-x-auto rounded-box border border-base-content/5 bg-base-100"
  >
    <div class="w-min-[900px]">
      <table class="table w-full">
        <thead class="font-medium text-base-content bg-gray-200">
          <tr class="">
            <th class="w-[30%]">Name</th>
            <th class="w-[20%] hidden sm:table-cell">Username</th>
            <th class="w-[25%] hidden md:table-cell">Email</th>
            <th class="w-[25%]">Check-in Time</th>
          </tr>
        </thead>
        <tbody>
          {#if isLoading}
            <tr>
              <td colspan="4" class="text-center py-4">
                <div class="loading loading-spinner loading-md"></div>
              </td>
            </tr>
          {:else if data.eventData.checkInUser.length > 0}
            {#each data.eventData.checkInUser as user}
              <tr class="hover:bg-base-200 border-t border-base-300">
                <td>
                  <p class="font-medium line-clamp-1">{user.owner_name}</p>
                </td>
                <td class="hidden sm:table-cell">
                  <p class="line-clamp-1">{user.username || "N/A"}</p>
                </td>
                <td class="hidden md:table-cell">
                  <p class="line-clamp-1">{user.email || "N/A"}</p>
                </td>
                <td>
                  <p class="line-clamp-1">
                    {formatDateTime(user.datetime)}
                  </p>
                </td>
              </tr>
            {/each}
          {:else}
            <tr>
              <td colspan="4" class="text-center">
                <p class="text-base-content/70">No check-ins found</p>
              </td>
            </tr>
          {/if}
        </tbody>
      </table>
    </div>
  </div>
  <Pagination
    pagination={data?.pagination}
    onPageChange={(pageNum: number) => loadPage(pageNum, searchQuery)}
    size="sm"
  />
</div>
