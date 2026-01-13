<script lang="ts">
	import type { Snippet } from 'svelte';
	import type { LayoutData } from './$types';
	import MenuMyTicketNav from '$lib/components/navbar/menuMyTicketNav.svelte';

	let { data, children }: { data: LayoutData; children: Snippet } = $props();
</script>

<main class={'flex flex-col gap-3.5 w-full items-start min-h-full max-w-screen overflow-y-auto'}>
	<MenuMyTicketNav />
	<div class="w-full">
		{@render children()}
	</div>
</main>
