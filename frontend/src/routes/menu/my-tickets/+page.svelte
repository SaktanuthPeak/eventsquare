<script lang="ts">
	import { WarningOctagon } from 'phosphor-svelte';
	import type { PageData } from './$types';
	import { fade } from 'svelte/transition';
	import TicketCard from '$lib/components/cards/TicketCards.svelte';

	let { data }: { data: PageData } = $props();
</script>

<div class="flex flex-col w-full">
	<div class="flex flex-row justify-between items-center my-2">
		<h1 class="text-2xl font-bold">My Tickets</h1>
	</div>

	{#if data?.tickets?.length}
		<div
			class="overflow-y-auto h-[70%] md:h-[90%] grid grid-cols-1 md:grid-cols-2 gap-3"
			transition:fade={{ duration: 300 }}
		>
			{#each data?.tickets as ticket}
				<TicketCard {ticket} />
			{/each}
		</div>
	{:else}
		<div
			class="flex flex-col justify-center items-center h-full w-full"
			transition:fade={{ duration: 300 }}
		>
			<div class="bg-primary/5 p-6 rounded-full mb-6">
				<WarningOctagon size={64} weight="light" class="text-primary/40" />
			</div>
			<h3 class="text-xl font-semibold mb-2">No Tickets</h3>
			<p class="text-base-content/70 text-center max-w-md mb-6">
				You don't have any tickets yet. If you have already purchased a ticket, please check
				your purchase history or wait for approval.
			</p>

		</div>
	{/if}
</div>
