<script lang="ts">
  import { onMount } from "svelte";
  import type { PageData } from "./$types";
  import OrganizerOwnerNav from "../organizerOwnerNav/+page.svelte";
  let { data }: { data: PageData } = $props();
</script>

<OrganizerOwnerNav orgNavData={data} />
<div
  class="overflow-x-auto border-base-content/5 bg-base-100 max-w-screen mt-[10px] px-[200px]"
>
  <h1 class="text-3xl font-extrabold text-start">Dashboard</h1>
  <div class="flex flex-col text-center justify-center py-[50px]"></div>
</div>
