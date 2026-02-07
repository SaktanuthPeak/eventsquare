<script lang="ts">
	import type { PageData } from './$types';
	import type { SubmitFunction } from '@sveltejs/kit';
	import { invalidateAll } from '$app/navigation';
	import { toast } from 'svelte-sonner';
	import ConfirmActionDialog from '$lib/components/ui/ConfirmActionDialog.svelte';

	let { data }: { data: PageData } = $props();

	type PendingDelete = { id: string; name: string } | null;
	let pendingDelete: PendingDelete = $state(null);
	let confirmDeleteDialog: { open: () => void; close: () => void } | null = $state(null);

	function openDeleteModal(event: { id: string; name?: string | null }) {
		pendingDelete = { id: event.id, name: event.name ?? 'this event' };
		confirmDeleteDialog?.open();
	}

	function closeDeleteModal() {
		confirmDeleteDialog?.close();
		pendingDelete = null;
	}

	const onDeleteEnhanced: SubmitFunction = () => {
		return async ({ result }: any) => {
			if (result?.type === 'success') {
				const payload = result.data as any;
				if (payload?.success) {
					toast.success(payload?.message ?? 'Event deleted');
					closeDeleteModal();
					await invalidateAll();
					return;
				}
				toast.error(payload?.message ?? 'Failed to delete event');
				return;
			}

			if (result?.type === 'failure') {
				toast.error((result.data as any)?.message ?? 'Failed to delete event');
				return;
			}

			toast.error('Failed to delete event');
		};
	};

	function toValidDate(value: unknown): Date | null {
		if (value instanceof Date) return Number.isNaN(value.getTime()) ? null : value;
		if (typeof value === 'string' || typeof value === 'number') {
			const parsed = new Date(value);
			return Number.isNaN(parsed.getTime()) ? null : parsed;
		}
		return null;
	}

	function formatDateTime(value: unknown): string {
		const dt = toValidDate(value);
		if (!dt) return '—';
		return new Intl.DateTimeFormat('en-GB', {
			year: 'numeric',
			month: 'short',
			day: '2-digit',
			hour: '2-digit',
			minute: '2-digit'
		}).format(dt);
	}
</script>

<div class="container mx-auto px-4 py-10">
	<div class="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
		<div>
			<h1 class="text-2xl font-bold">Events</h1>
			<p class="mt-1 text-base-content/70">Manage events: view, create, and edit.</p>
		</div>
		<a class="btn btn-primary" href="/admin/create-event">Create event</a>
	</div>

	<div class="mt-6">
		<form method="GET" class="flex gap-2 items-center">
			<input
				class="input input-bordered w-full max-w-md"
				type="search"
				name="search"
				placeholder="Search by name…"
				value={data.search}
			/>
			<button class="btn btn-outline" type="submit">Search</button>
		</form>
	</div>

	<div class="mt-6 overflow-x-auto rounded-lg border border-base-300 bg-base-100">
		<table class="table">
			<thead>
				<tr>
					<th>Name</th>
					<th>Type</th>
					<th>Start</th>
					<th>End</th>
					<th>Location</th>
					<th class="text-right">Actions</th>
				</tr>
			</thead>
			<tbody>
				{#if data.events.length === 0}
					<tr>
						<td colspan="6" class="py-10 text-center text-base-content/70">No events found.</td>
					</tr>
				{:else}
					{#each data.events as event (event.id)}
						<tr>
							<td class="font-medium">{event.name}</td>
							<td>{event.event_type}</td>
							<td>{formatDateTime(event.start_date)}</td>
							<td>{formatDateTime(event.end_date)}</td>
							<td>{event.location ?? '—'}</td>
							<td class="text-right">
								<div class="flex justify-end gap-2">
									<a class="btn btn-sm btn-ghost" href={`/events/${event.id}`}>View</a>
									<a class="btn btn-sm btn-outline" href={`/admin/events/${event.id}/tickets`}>Tickets</a>
									<a class="btn btn-sm btn-secondary" href={`/admin/events/${event.id}/edit`}>Edit</a>
									<button
										type="button"
										class="btn btn-sm btn-error"
										onclick={() => openDeleteModal(event)}
									>
										Delete
									</button>
								</div>
							</td>
						</tr>
					{/each}
				{/if}
			</tbody>
		</table>
	</div>
</div>

<ConfirmActionDialog
	bind:this={confirmDeleteDialog}
	title="Delete event"
	description={`Are you sure you want to delete ${pendingDelete?.name ?? 'this event'}? This action cannot be undone.`}
	action="?/delete"
	hiddenFields={[{ name: 'event_id', value: pendingDelete?.id ?? '' }]}
	confirmText="Delete"
	cancelText="Cancel"
	confirmClass="btn btn-error"
	confirmDisabled={!pendingDelete?.id}
	onResult={onDeleteEnhanced}
/>
