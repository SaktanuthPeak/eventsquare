<script lang="ts">
  import type { Snippet } from "svelte";
  import type { LayoutData } from "./$types";
  import StaffNavbar from "./staffNavbar/+page.svelte";

  let { data, children }: { data: LayoutData; children: Snippet } = $props();
</script>

<div class="flex flex-col min-h-screen mt-[25px]">
  <StaffNavbar {data} />
  <main class="">
    {@render children()}
  </main>
</div>
