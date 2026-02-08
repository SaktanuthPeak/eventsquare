<script lang="ts">
	import type { PageData } from './$types';
	import EventForm from '$lib/components/ui/EventForm.svelte';
	import { superForm } from 'sveltekit-superforms';
	import { zodClient } from 'sveltekit-superforms/adapters';
	import { eventFormSchema } from '$lib/schemas/eventSchema';
	import { toast } from 'svelte-sonner';
	import { goto, invalidateAll } from '$app/navigation';
	import TicketTypeManager from '$lib/components/admin/TicketTypeManager.svelte';

	let { data }: { data: PageData } = $props();

	const form = $derived.by(() =>
		superForm(data.form as any, {
			validators: zodClient(eventFormSchema as any),
			customValidity: true,
			dataType: 'form',
			onResult: async ({ result }) => {
				if (result.type === 'success') {
					toast.success('Event updated successfully!');
					await goto('/admin/events', { invalidateAll: true });
				} else if (result.type === 'failure') {
					toast.error(result.data?.message || 'Failed to update event.');
				}
			}
		})
	);

</script>

<div class="mx-auto py-16 px-4 md:px-12 lg:px-50">
	<div class="mb-6">
		<div class="flex flex-col gap-3 md:flex-row md:items-end md:justify-between">
			<div>
				<h1 class="text-4xl font-bold">Edit event</h1>
				<p class="mt-2 text-base-content/70">Update event details and save changes.</p>
			</div>
			{#if data.event}
				<div class="flex gap-2">
					<a class="btn btn-outline" href={`/admin/events/${data.event.id}/edit/upload-image`}
						>Upload image</a
					>
					<a class="btn btn-ghost" href={`/admin/events/${data.event.id}/tickets`}>Tickets</a>
				</div>
			{/if}
		</div>
	</div>
	<EventForm {form} mode="edit" />

	{#if data.event}
		<div class="mt-10">
			<div class="mb-4">
				<h2 class="text-2xl font-bold">Tickets</h2>
				<p class="mt-1 text-base-content/70">Created ticket types (read-only).</p>
			</div>
			<TicketTypeManager ticketTypes={data.event.ticket_types ?? []} />
		</div>
	{/if}
</div>
