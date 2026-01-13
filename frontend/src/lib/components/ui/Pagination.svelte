<script lang="ts">
  import type { IPaginationData } from "$lib/models/pagination";

  let {
    pagination = $bindable<IPaginationData>({
      currentPage: 1,
      totalPages: 1,
      totalItems: 0,
      itemsPerPage: 10,
    }),
    onPageChange = $bindable((pageNumber: number) => {}),
    maxVisiblePages = $bindable(5),
    size = $bindable<"sm" | "md" | "lg">("md"),
    showGoToPage = $bindable(false),
  } = $props();

  let goToPageInput = $state(pagination.currentPage.toString());
  let pageNumbers = $derived(
    calculatePageNumbers(
      pagination.currentPage,
      pagination.totalPages,
      maxVisiblePages
    )
  );

  let sizeClass = $derived(
    size === "sm" ? "btn-sm" : size === "lg" ? "btn-lg" : "btn-md"
  );

  function calculatePageNumbers(
    currentPage: number,
    totalPages: number,
    maxVisible: number
  ): { value: number; isEllipsis: boolean }[] {
    const result: { value: number; isEllipsis: boolean }[] = [];

    // Always show first page
    result.push({ value: 1, isEllipsis: false });

    // For large page counts, we need a more sophisticated approach
    if (totalPages <= maxVisible + 2) {
      // Show all pages if there aren't too many (plus first and last)
      for (let i = 2; i < totalPages; i++) {
        result.push({ value: i, isEllipsis: false });
      }
    } else {
      // Calculate the window of pages to show
      let startPage: number;
      let endPage: number;
      const sidePages = Math.floor((maxVisible - 1) / 2);

      if (currentPage <= sidePages + 1) {
        // Near the beginning - show first {maxVisible} pages and then ellipsis
        startPage = 2;
        endPage = maxVisible;

        for (let i = startPage; i <= endPage; i++) {
          result.push({ value: i, isEllipsis: false });
        }
        result.push({ value: -1, isEllipsis: true }); // Ellipsis
      } else if (currentPage >= totalPages - sidePages) {
        // Near the end - show ellipsis and then last {maxVisible} pages
        startPage = totalPages - maxVisible + 1;
        endPage = totalPages - 1;

        result.push({ value: -1, isEllipsis: true }); // Ellipsis
        for (let i = startPage; i <= endPage; i++) {
          result.push({ value: i, isEllipsis: false });
        }
      } else {
        // In the middle - show ellipsis on both sides
        result.push({ value: -1, isEllipsis: true }); // Left ellipsis

        // Show pages around current page
        for (
          let i = currentPage - sidePages;
          i <= currentPage + sidePages;
          i++
        ) {
          if (i > 1 && i < totalPages) {
            result.push({ value: i, isEllipsis: false });
          }
        }

        result.push({ value: -1, isEllipsis: true }); // Right ellipsis
      }
    }

    // Always show last page if not already included
    if (totalPages > 1) {
      result.push({ value: totalPages, isEllipsis: false });
    }

    return result;
  }

  function handleGoToPage() {
    const pageNum = parseInt(goToPageInput, 10);
    if (!isNaN(pageNum) && pageNum >= 1 && pageNum <= pagination.totalPages) {
      onPageChange(pageNum);
    } else {
      // Reset input to current page if invalid
      goToPageInput = pagination.currentPage.toString();
    }
  }
</script>

{#if pagination.totalPages > 1}
  <div class="flex flex-col items-center gap-3 my-4">
    <div class="join gap-[5px]">
      <!-- First page button -->
      <button
        class="join-item rounded-full btn {sizeClass}"
        disabled={pagination.currentPage === 1}
        onclick={() => onPageChange(1)}
        aria-label="First page"
      >
        «
      </button>

      <!-- Previous page button -->
      <button
        class="join-item rounded-full btn {sizeClass}"
        disabled={pagination.currentPage === 1}
        onclick={() => onPageChange(pagination.currentPage - 1)}
        aria-label="Previous page"
      >
        ‹
      </button>

      <!-- Page numbers and ellipses -->
      {#each pageNumbers as item}
        {#if item.isEllipsis}
          <span class="join-item {sizeClass} self-end btn-disabled no-animation"
            >...</span
          >
        {:else}
          <button
            class="join-item rounded-full btn {sizeClass} {pagination.currentPage ===
            item.value
              ? 'btn-primary'
              : ''}"
            onclick={() => onPageChange(item.value)}
            aria-current={pagination.currentPage === item.value
              ? "page"
              : undefined}
            aria-label="Page {item.value}"
          >
            {item.value}
          </button>
        {/if}
      {/each}

      <!-- Next page button -->
      <button
        class="join-item rounded-full btn {sizeClass}"
        disabled={pagination.currentPage === pagination.totalPages}
        onclick={() => onPageChange(pagination.currentPage + 1)}
        aria-label="Next page"
      >
        ›
      </button>

      <!-- Last page button -->
      <button
        class="join-item rounded-full btn {sizeClass}"
        disabled={pagination.currentPage === pagination.totalPages}
        onclick={() => onPageChange(pagination.totalPages)}
        aria-label="Last page"
      >
        »
      </button>
    </div>

    <!-- Pagination info and go to page -->
    <div class="flex items-center gap-4 text-sm">
      <span>Page {pagination.currentPage} of {pagination.totalPages}</span>

      {#if showGoToPage || pagination.totalPages > 10}
        <div class="flex items-center gap-2">
          <span>Go to:</span>
          <input
            type="number"
            bind:value={goToPageInput}
            min="1"
            max={pagination.totalPages}
            class="input input-bordered input-sm w-16"
            onkeydown={(e) => e.key === "Enter" && handleGoToPage()}
          />
          <button class="btn btn-sm btn-primary" onclick={handleGoToPage}>
            Go
          </button>
        </div>
      {/if}
    </div>
  </div>
{/if}
