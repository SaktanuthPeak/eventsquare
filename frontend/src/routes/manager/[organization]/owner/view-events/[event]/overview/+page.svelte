<script lang="ts">
  import TextInput from "$lib/components/ui/forms/TextInput.svelte";
  import type { PageData } from "./$types";

  let { data }: { data: PageData } = $props();
</script>

<div class="overflow-x-auto border-base-content/5 bg-base-100 max-w-screen">
  <h2 class="text-2xl font-bold text-start p-4">DashBoard</h2>
  <div class="flex flex-row justify-between w-full"></div>
  <div class="flex flex-col max-h-[825x] gap-[5px]">
    <div class="card h-[160px]">
      <div class="card-body">
        <h2 class="card-title">Order ID: 123456</h2>
      </div>
    </div>
  </div>
</div>
