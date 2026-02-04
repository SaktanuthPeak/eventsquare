<script lang="ts">
	import type { PageData } from './$types';
	import { Calendar, Buildings, Clock, WarningOctagon } from 'phosphor-svelte';
	import { formatDateTime } from '$lib/utils/date-utils';
	import { fade } from 'svelte/transition';

	let { data }: { data: PageData } = $props();
</script>

<div class="flex flex-col w-full">
	<div class="flex flex-row justify-between items-center mb-6">
		<h1 class="text-2xl font-bold">My Check-in History</h1>
		{#if data?.checkedInHistory?.length > 0}
			<p class="text-base-content/70">
				Total check-ins: <span class="font-semibold">{data.checkedInHistory.length}</span>
			</p>
		{/if}
	</div>

	{#if data?.checkedInHistory?.length > 0}
		<div
			class="grid grid-cols-1 sm:grid-cols-2 gap-4 max-h-[70vh] overflow-y-auto pr-2 pb-4"
			transition:fade={{ duration: 300 }}
		>
			{#each data?.checkedInHistory as checkIn}
				<div
					class="card bg-gradient-to-tl to-45% from-success/20 hover:shadow-md transition-all border border-primary/10"
				>
					<div class="card-body p-4">
						<h2 class="card-title text-lg truncate w-full">{checkIn.event_name}</h2>
						<div class="badge badge-success text-success-content font-medium">Checked In</div>

						<div class="flex items-center gap-2 mt-2">
							<Calendar size={18} class="text-primary flex-shrink-0" />
							<span class="text-sm truncate">{formatDateTime(checkIn.created_date)}</span>
						</div>

						{#if checkIn.location}
							<div class="flex items-center gap-2">
								<Buildings size={18} class="text-primary flex-shrink-0" />
								<span class="text-sm truncate">{checkIn.location}</span>
							</div>
						{/if}
					</div>
				</div>
			{/each}
		</div>
	{:else}
		<div
			class="flex flex-col justify-center items-center py-16 rounded-xl"
			transition:fade={{ duration: 300 }}
		>
			<div class=" mb-6">
				<WarningOctagon size={64} weight="light" class="text-primary/70" />
			</div>
			<h3 class="text-xl font-semibold mb-2">No Check-in History</h3>
			<p class="text-base-content/70 text-center max-w-md mb-6">
				You haven't checked in to any events yet. When you check in to an event, it will appear
				here.
			</p>
			<a href="/events" class="btn btn-primary"> Browse Events </a>
		</div>
	{/if}
</div>
