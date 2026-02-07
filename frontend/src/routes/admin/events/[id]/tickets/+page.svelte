<script lang="ts">
	import type { PageData } from './$types';
	import TicketTypeManager from '$lib/components/admin/TicketTypeManager.svelte';

	let { data }: { data: PageData } = $props();

	const event = $derived(data.event);
	const tickets = $derived(data.event?.ticket_types ?? []);
</script>

<div class="container mx-auto px-4 py-10">
	<div class="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
		<div>
			<h1 class="text-2xl font-bold">Ticket management</h1>
			<p class="mt-1 text-base-content/70">
				{#if event}{event.name}{:else}Event{/if} — ticket types.
			</p>
		</div>
		<div class="flex gap-2">
			<a class="btn btn-ghost" href="/admin/events">Back</a>
			{#if event}
				<a class="btn btn-outline" href={`/admin/events/${event.id}/edit`}>Edit event</a>
			{/if}
		</div>
	</div>

	{#if !event}
		<div class="mt-8 alert alert-error">Event not found.</div>
	{:else}
		<div class="mt-8">
			<TicketTypeManager ticketTypes={tickets} />
		</div>
	{/if}
</div>
