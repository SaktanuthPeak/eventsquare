<script lang="ts">
  import type { Snippet } from "svelte";
  import type { LayoutData } from "./$types";
  import { page } from "$app/stores";
  import ManagerNav from "./[organization]/owner/managerNav/+page.svelte";

  let { data, children }: { data: LayoutData; children: Snippet } = $props();
</script>

<div class="flex flex-col min-h-screen">
  <ManagerNav orgAndUserData={data} />

  <main class="mt-[25px]">
    {@render children()}
  </main>
</div>
