<script lang="ts">
	import type { PageData } from './$types';
	import TicketTypeManager from '$lib/components/admin/TicketTypeManager.svelte';
	import { fileProxy, superForm } from 'sveltekit-superforms';
	import { zodClient } from 'sveltekit-superforms/adapters';
	import { imageUploadSchema } from '$lib/schemas/imageUploadSchema';
	import FileInput from '$lib/components/ui/forms/FileInput.svelte';
	import FormErrorSummary from '$lib/components/ui/forms/FormErrorSummary.svelte';
	import { toast } from 'svelte-sonner';
	import { invalidateAll } from '$app/navigation';

	let { data }: { data: PageData } = $props();

	const event = $derived(data.event);
	const tickets = $derived(data.event?.ticket_types ?? []);

	const imageForm = $derived.by(() =>
		superForm(data.imageForm as any, {
			validators: zodClient(imageUploadSchema as any),
			customValidity: true,
			dataType: 'form',
			onResult: async ({ result }) => {
				if (result.type === 'success') {
					toast.success('Image uploaded');
					await invalidateAll();
				} else if (result.type === 'failure') {
					toast.error((result.data as any)?.message || 'Image upload failed');
				}
			}
		})
	);

	const enhance = $derived(imageForm.enhance);
	const allErrors = $derived(imageForm.allErrors);
	const file = $derived(fileProxy(imageForm, 'image'));
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
				<a class="btn btn-outline" href={`/admin/events/${event.id}/edit/upload-image`}
					>Upload image</a
				>
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
