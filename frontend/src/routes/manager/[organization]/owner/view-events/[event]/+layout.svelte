<script lang="ts">
  import type { Snippet } from "svelte";
  import type { LayoutData } from "./$types";
  import EventNavbar from "./eventNav/+page.svelte";
  import PublicEventNavbar from "./publicEventNav/+page.svelte";

  let { data, children }: { data: LayoutData; children: Snippet } = $props();
</script>

<div class="flex flex-col min-h-screen">
  {#if data.eventData?.event_type === "private"}
    <EventNavbar {data} />
  {:else}
    <PublicEventNavbar {data} />
  {/if}

  <main class="mt-[20px] px-[200px]">
    {@render children()}
  </main>
</div>
