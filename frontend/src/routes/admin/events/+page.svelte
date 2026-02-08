<script lang="ts">
	import type { PageData } from './$types';
	import type { SubmitFunction } from '@sveltejs/kit';
	import { invalidateAll } from '$app/navigation';
	import { toast } from 'svelte-sonner';
	import ConfirmActionDialog from '$lib/components/ui/ConfirmActionDialog.svelte';
	import {
		CalendarBlank,
		MapPin,
		Plus,
		Ticket,
		Users,
		PencilSimple,
		Trash,
		MagnifyingGlass
	} from 'phosphor-svelte';

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

	const totalEvents = $derived(typeof data.total === 'number' ? data.total : data.events.length);
</script>

<div class="container mx-auto px-4 py-10 space-y-6">
	<div class="card bg-base-100 border border-base-200 shadow-sm">
		<div class="card-body p-6 md:p-8">
			<div class="flex flex-col gap-5 md:flex-row md:items-center md:justify-between">
				<div class="space-y-1">
					<h1 class="text-2xl md:text-3xl font-bold">Events</h1>
					<p class="text-base-content/70">Manage events: view, create, and edit.</p>
				</div>
				<a class="btn btn-primary gap-2" href="/admin/create-event">
					<Plus size={18} />
					Create event
				</a>
			</div>

			<div class="mt-5 grid grid-cols-1 sm:grid-cols-3 gap-3">
				<div class="rounded-xl border border-base-200 bg-base-100 p-4">
					<div class="flex items-center justify-between">
						<div>
							<p class="text-sm text-base-content/60">Total events</p>
							<p class="text-2xl font-bold">{totalEvents}</p>
						</div>
						<div class="rounded-xl bg-primary/10 p-3">
							<CalendarBlank size={22} class="text-primary" />
						</div>
					</div>
				</div>
				<div class="rounded-xl border border-base-200 bg-base-100 p-4">
					<div class="flex items-center justify-between">
						<div>
							<p class="text-sm text-base-content/60">This page</p>
							<p class="text-2xl font-bold">{data.events.length}</p>
						</div>
						<div class="rounded-xl bg-secondary/10 p-3">
							<Users size={22} class="text-secondary" />
						</div>
					</div>
				</div>
				<div class="rounded-xl border border-base-200 bg-base-100 p-4">
					<div class="flex items-center justify-between">
						<div>
							<p class="text-sm text-base-content/60">Page</p>
							<p class="text-2xl font-bold">{data.page}</p>
						</div>
						<div class="rounded-xl bg-success/10 p-3">
							<Ticket size={22} class="text-success" />
						</div>
					</div>
				</div>
			</div>

			<!-- Keep existing search only (no additional filters) -->
			<form method="GET" class="mt-5 flex flex-col sm:flex-row gap-2 sm:items-center">
				<label class="input input-bordered flex items-center gap-2 w-full sm:max-w-md">
					<MagnifyingGlass size={18} class="opacity-70" />
					<input
						type="search"
						name="search"
						class="grow"
						placeholder="Search by name…"
						value={data.search}
					/>
				</label>
				<button class="btn btn-outline" type="submit">Search</button>
				{#if data.search}
					<a class="btn btn-ghost" href="/admin/events">Clear</a>
				{/if}
			</form>
		</div>
	</div>

	{#if data.events.length === 0}
		<div class="card bg-base-100 border border-base-200 shadow-sm">
			<div class="card-body p-10 text-center">
				<div class="mx-auto mb-4 rounded-2xl bg-base-200 p-4 w-fit">
					<CalendarBlank size={44} class="opacity-70" />
				</div>
				<h2 class="text-xl font-semibold">No events found</h2>
				<p class="mt-2 text-base-content/70">Create a new event, or clear the search.</p>
				<div class="mt-6 flex justify-center gap-2">
					<a class="btn btn-primary gap-2" href="/admin/create-event">
						<Plus size={18} />
						Create event
					</a>
					<a class="btn btn-ghost" href="/events">View public events</a>
				</div>
			</div>
		</div>
	{:else}
		<!-- Desktop table -->
		<div class="hidden md:block overflow-x-auto rounded-xl border border-base-200 bg-base-100 shadow-sm">
			<table class="table table-zebra">
				<thead>
					<tr>
						<th>Event</th>
						<th>Type</th>
						<th>When</th>
						<th>Location</th>
						<th class="text-right">Actions</th>
					</tr>
				</thead>
				<tbody>
					{#each data.events as event (event.id)}
						<tr class="hover">
							<td>
								<div class="flex flex-col">
									<a class="font-semibold link link-hover" href={`/events/${event.id}`}>{event.name}</a>
									<span class="text-xs text-base-content/60">ID: {event.id}</span>
								</div>
							</td>
							<td><span class="badge badge-ghost">{event.event_type}</span></td>
							<td>
								<div class="text-sm">
									<div>{formatDateTime(event.start_date)}</div>
									<div class="text-base-content/60">to {formatDateTime(event.end_date)}</div>
								</div>
							</td>
							<td>
								<div class="flex items-center gap-2">
									<MapPin size={16} class="opacity-70" />
									<span class="truncate max-w-60">{event.location ?? '—'}</span>
								</div>
							</td>
							<td class="text-right">
								<div class="flex justify-end gap-2">
									<a class="btn btn-sm btn-ghost gap-2" href={`/admin/events/${event.id}/participants`}>
										<Users size={16} /> Participants
									</a>
									<a class="btn btn-sm btn-outline gap-2" href={`/admin/events/${event.id}/tickets`}>
										<Ticket size={16} /> Tickets
									</a>
									<a class="btn btn-sm btn-secondary gap-2" href={`/admin/events/${event.id}/edit`}>
										<PencilSimple size={16} /> Edit
									</a>
									<button
										type="button"
										class="btn btn-sm btn-error gap-2"
										onclick={() => openDeleteModal(event)}
									>
										<Trash size={16} /> Delete
									</button>
								</div>
							</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>

		<!-- Mobile cards -->
		<div class="md:hidden grid grid-cols-1 gap-3">
			{#each data.events as event (event.id)}
				<div class="card bg-base-100 border border-base-200 shadow-sm">
					<div class="card-body p-5">
						<div class="flex items-start justify-between gap-3">
							<div class="min-w-0">
								<a class="text-lg font-semibold link link-hover truncate" href={`/events/${event.id}`}>
									{event.name}
								</a>
								<div class="mt-1 flex gap-2 items-center flex-wrap">
									<span class="badge badge-ghost">{event.event_type}</span>
									<span class="text-xs text-base-content/60">ID: {event.id}</span>
								</div>
							</div>
						</div>

						<div class="mt-3 text-sm space-y-2">
							<div class="flex items-center gap-2">
								<CalendarBlank size={16} class="opacity-70" />
								<span>{formatDateTime(event.start_date)} – {formatDateTime(event.end_date)}</span>
							</div>
							<div class="flex items-center gap-2">
								<MapPin size={16} class="opacity-70" />
								<span class="truncate">{event.location ?? '—'}</span>
							</div>
						</div>

						<div class="mt-4 flex flex-wrap gap-2">
							<a class="btn btn-sm btn-ghost gap-2" href={`/admin/events/${event.id}/participants`}>
								<Users size={16} /> Participants
							</a>
							<a class="btn btn-sm btn-outline gap-2" href={`/admin/events/${event.id}/tickets`}>
								<Ticket size={16} /> Tickets
							</a>
							<a class="btn btn-sm btn-secondary gap-2" href={`/admin/events/${event.id}/edit`}>
								<PencilSimple size={16} /> Edit
							</a>
							<button type="button" class="btn btn-sm btn-error gap-2" onclick={() => openDeleteModal(event)}>
								<Trash size={16} /> Delete
							</button>
						</div>
					</div>
				</div>
			{/each}
		</div>
	{/if}
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
