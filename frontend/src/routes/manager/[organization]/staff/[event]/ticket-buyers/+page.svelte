<script lang="ts">
  import type { PageData } from "./$types";
  import { page } from "$app/stores";
  import { goto } from "$app/navigation";
  import { onMount } from "svelte";

  let { data }: { data: PageData } = $props();
  let isLoading = $state(true);
  let searchQuery = $state("");
  let searchTimeout: number;

  function loadPage(pageNum: number, search: string = searchQuery) {
    const url = new URL($page.url);
    url.searchParams.set("page", pageNum.toString());
    if (search) {
      url.searchParams.set("search", search);
    } else {
      url.searchParams.delete("search");
    }
    goto(url.toString(), { keepFocus: true }).finally(() => {
      isLoading = false;
    });
  }

  onDestroy(() => {
    if (searchTimeout) {
      clearTimeout(searchTimeout);
    }
  });

  onMount(() => {
    searchQuery = $page.url.searchParams.get("search") || "";
  });
</script>

<div class="flex flex-col min-h-screen">
  <div class=" px-[200px]">
    <h1 class="text-2xl font-bold">
      Ticket Buyers for
      <span class="text-accent font-bold">{data?.eventData?.title}</span>
    </h1>
    <p class="text-lg"></p>
  </div>
  {#if data?.pagination && data.pagination.totalPages > 1}
    <div class="flex justify-center mt-4">
      <div class="join">
        <button
          class="join-item btn"
          disabled={data.pagination.currentPage === 1}
          onclick={() => loadPage(data.pagination.currentPage - 1)}
        >
          &laquo;
        </button>

        {#each Array(Math.min(data.pagination.totalPages, 5)) as _, i}
          {@const pageNum =
            data.pagination.currentPage > 2 && data.pagination.totalPages > 5
              ? data.pagination.currentPage - 2 + i
              : i + 1}

          {#if pageNum <= data.pagination.totalPages}
            <button
              class="join-item btn {data.pagination.currentPage === pageNum
                ? 'btn-primary'
                : ''}"
              onclick={() => loadPage(pageNum)}
            >
              {pageNum}
            </button>
          {/if}
        {/each}

        <button
          class="join-item btn"
          disabled={data.pagination.currentPage === data.pagination.totalPages}
          onclick={() => loadPage(data.pagination.currentPage + 1)}
        >
          &raquo;
        </button>
      </div>
    </div>
  {/if}
  <div class="mt-[20px] px-[200px]"></div>
</div>
