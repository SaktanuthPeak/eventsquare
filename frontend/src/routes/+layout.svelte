<script lang="ts">
  import { Toaster } from "svelte-sonner";
  import "../style.css";
  let { children } = $props();
</script>

<div class="w-full overflow-x-hidden scroll-smooth">
  <Toaster richColors position="top-center" />
  {@render children()}
</div>
