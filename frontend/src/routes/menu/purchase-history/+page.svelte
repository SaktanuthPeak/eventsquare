<script lang="ts">
	import { User, WarningOctagon, Receipt, Calendar } from 'phosphor-svelte';
	import type { PageData } from './$types';
	import { fade } from 'svelte/transition';
	import { cn } from '$lib/utils/tw-utils';
	import { formatDateTime } from '$lib/utils/date-utils';
	import OrderCards from '$lib/components/cards/OrderCards.svelte';

	let { data }: { data: PageData } = $props();
	let activeTab = $state('pending');

	const filteredOrders = $derived(
		data.orders?.filter((order) => {
			if (activeTab === 'pending') {
				return (
					typeof order.order_status === 'string' &&
					['pending', 'not_paid'].includes(order.order_status)
				);
			} else {
				return (
					typeof order.order_status === 'string' &&
					['completed', 'cancelled'].includes(order.order_status)
				);
			}
		}) || []
	);
</script>

<div class="flex flex-col w-full mb-[20px]">
	<h1 class="text-2xl font-bold mb-2">Purchase History</h1>

	<!-- Tab Navigation -->
	<div class="mb-6">
		<div class="inline-flex p-1 gap-2 rounded-xl shadow-sm outline-1 outline-base-200">
			<button
				onclick={() => (activeTab = 'pending')}
				class="relative px-4 py-2 text-sm font-medium rounded-lg transition-all duration-200 ease-in-out {activeTab ===
				'pending'
					? 'text-white'
					: 'text-gray-600 hover:text-primary'}"
			>
				<span class="relative z-10">Not Approved</span>
				{#if activeTab === 'pending'}
					<div
						class="absolute inset-0 bg-gradient-to-r from-pink-400 to-secondary rounded-lg shadow-lg"
						transition:fade={{ duration: 150 }}
					></div>
				{/if}
			</button>

			<button
				onclick={() => (activeTab = 'completed')}
				class="relative px-6 py-3 text-sm font-medium rounded-lg transition-all duration-200 ease-in-out {activeTab ===
				'completed'
					? 'text-white'
					: 'text-gray-600 hover:text-primary'}"
			>
				<span class="relative z-10">Approved/Cancelled</span>
				{#if activeTab === 'completed'}
					<div
						class="absolute inset-0 bg-gradient-to-r from-pink-400 to-secondary rounded-lg shadow-lg"
						transition:fade={{ duration: 150 }}
					></div>
				{/if}
			</button>
		</div>
	</div>

	<!-- Orders List -->
	{#if filteredOrders.length > 0}
		<div
			class="flex flex-col gap-4 overflow-y-auto w-full h-[70%] md:h-[90%] rounded-2xl p-4"
			transition:fade={{ duration: 150 }}
		>
			{#each filteredOrders as order}
				<OrderCards {order} />
			{/each}
		</div>
	{:else}
		<div
			class="flex flex-col justify-center items-center w-full py-16"
			transition:fade={{ duration: 150 }}
		>
			<WarningOctagon size={64} weight="light" class="text-gray-500 mb-4" />
			<span class="text-gray-500 text-center">
				{activeTab === 'pending'
					? "You don't have any pending orders."
					: "You don't have any approved or cancelled orders yet."}
			</span>
		</div>
	{/if}
</div>
