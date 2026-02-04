<script lang="ts">
	import { MapPin, Ticket } from 'phosphor-svelte';
	import { fade } from 'svelte/transition';
	import { env } from '$env/dynamic/public';

	let { event } = $props();
</script>

<a
	href={`/events/${event?.id}`}
	class="rounded-2xl hover:shadow-lg transition-shadow w-[180px] h-[360px] bg-base-100 shadow-md"
	transition:fade={{ duration: 200 }}
>
	<div class="h-[240px]">
		{#if event?.image_url}
			<img
				src={`${env.PUBLIC_API_URL}/v1/events/image/${event?.image.file_id}`}
				alt={event?.title}
				class="w-full h-full object-cover rounded-t-2xl"
			/>
		{:else}
			<div class="w-full h-full bg-base-300 flex items-center justify-center rounded-t-2xl">
				<h1 class="text-lg font-medium text-base-content/70">No Image</h1>
			</div>
		{/if}
	</div>
	<div
		class="text-sm bg-gradient-to-tr from-accent to-purple-600 text-white h-[25px] w-[80%] px-2 flex text-center justify-center line-clamp-1 font-bold rounded-br-2xl py-0.5"
	>
		{#if new Date(event?.start_date).toISOString().split('T')[0] === new Date(event?.end_date)
				.toISOString()
				.split('T')[0]}
			{new Intl.DateTimeFormat('en-UK', {
				year: 'numeric',
				month: 'short',
				day: 'numeric',
				timeZone: 'UTC'
			}).format(event?.start_date)}
		{:else}
			{new Intl.DateTimeFormat('en-UK', {
				month: 'short',
				day: 'numeric',
				timeZone: 'UTC'
			}).format(event?.start_date)} -

			{new Intl.DateTimeFormat('en-UK', {
				month: 'short',
				day: 'numeric',
				timeZone: 'UTC'
			}).format(event?.end_date)}
		{/if}
	</div>
	<div class="px-4 py-2 flex flex-col gap-2 h-[70px]">
		<h2 class="text-md items-start line-clamp-2 font-bold h-[30px] leading-4">
			{event?.title}
		</h2>

		<div class="  flex flex-row items-center gap-1 h-[20px]">
			<div class="flex items-center justify-center">
				<MapPin weight="fill" size={16} class="text-accent" />
			</div>
			<span class="text-base-content/70 text-sm truncate">
				{event?.location}
			</span>
		</div>
	</div>

	<div class="items-center flex flex-row w-full">
		<div
			class="btn btn-secondary rounded-t-none rounded-b-2xl border-0 outline-0 px-2 py-1 h-full w-full text-sm"
		>
			<Ticket size={18} weight="bold" />Buy Tickets
		</div>
	</div>
</a>
