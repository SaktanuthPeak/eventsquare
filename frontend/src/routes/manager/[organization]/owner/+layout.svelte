<script lang="ts">
  import type { Snippet } from "svelte";
  import type { LayoutData } from "./$types";

  let { children }: { data: LayoutData; children: Snippet } = $props();
</script>

<div class="flex flex-col min-h-screen">
  <main class="mt-[25px]">
    {@render children()}
  </main>
</div>
