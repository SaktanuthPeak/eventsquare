<script lang="ts">
	import { List, X } from 'phosphor-svelte';

	let { isOpen = $bindable(false) } = $props();

	export function toggleMenu() {
		isOpen = !isOpen;
	}
</script>

<button
	class="btn btn-ghost btn-circle md:hidden"
	aria-label={isOpen ? 'Close menu' : 'Open menu'}
	onclick={toggleMenu}
>
	{#if isOpen}
		<X size={24} weight="bold" />
	{:else}
		<List size={24} weight="bold" />
	{/if}
</button>
