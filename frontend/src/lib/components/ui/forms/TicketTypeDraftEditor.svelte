<script lang="ts">
	type TicketDraft = {
		ticket_id?: string | number | null;
		name: string;
		total: number;
		price: number;
		remaining?: number;
	};

	let {
		json = $bindable('[]'),
		initial,
		disabled = false,
		title = 'Ticket Types',
		subtitle = 'You can add more than 1 ticket type. Remaining will start equal to Total.'
	} = $props<{
		json?: string;
		initial?: unknown;
		disabled?: boolean;
		title?: string;
		subtitle?: string;
	}>();

	let ticketDrafts = $state<TicketDraft[]>([{ name: '', total: 1, price: 0 }]);
	let initialized = $state(false);

	function addTicketDraft() {
		ticketDrafts = [...ticketDrafts, { name: '', total: 1, price: 0 }];
	}

	function removeTicketDraft(index: number) {
		ticketDrafts = ticketDrafts.filter((_, i) => i !== index);
		if (ticketDrafts.length === 0) ticketDrafts = [{ name: '', total: 1, price: 0 }];
	}

	function normalizedTicketTypes(): Array<{
		ticket_id?: string | number | null;
		name: string;
		total: number;
		price: number;
		remaining: number;
	}> {
		return ticketDrafts
			.map((t) => ({
				ticket_id: t.ticket_id,
				name: String(t.name ?? '').trim(),
				total: Number(t.total ?? 0),
				price: Number(t.price ?? 0),
				remaining: Math.min(
					Number(t.remaining ?? t.total ?? 0),
					Number(t.total ?? 0)
				)
			}))
			.filter((t) => t.name.length > 0);
	}

	function coerceDrafts(value: unknown): TicketDraft[] {
		if (!value) return [];
		let parsed: unknown = value;
		if (typeof value === 'string') {
			try {
				parsed = JSON.parse(value);
			} catch {
				return [];
			}
		}
		if (!Array.isArray(parsed)) return [];

		return parsed
			.map((t: any) => ({
				ticket_id: t?.ticket_id ?? t?.id ?? undefined,
				name: String(t?.name ?? '').trim(),
				total: Number(t?.total ?? 1),
				price: Number(t?.price ?? 0),
				remaining: t?.remaining !== undefined ? Number(t.remaining) : undefined
			}))
			.filter((t) => t.name.length > 0);
	}

	$effect(() => {
		if (initialized) return;
		const seed = initial ?? json;
		const drafts = coerceDrafts(seed);
		if (drafts.length > 0) {
			ticketDrafts = drafts;
		}
		initialized = true;
	});

	$effect(() => {
		json = JSON.stringify(normalizedTicketTypes());
	});
</script>

<div class="space-y-4 rounded-lg border border-primary/20 p-6">
	<div class="flex items-center justify-between gap-3">
		<div>
			<h3 class="text-lg font-semibold text-gray-700">{title}</h3>
			{#if subtitle}
				<p class="mt-1 text-sm text-base-content/60">{subtitle}</p>
			{/if}
		</div>

		<button type="button" class="btn btn-sm btn-outline" onclick={addTicketDraft} disabled={disabled}>
			Add ticket
		</button>
	</div>

	<div class="space-y-3">
		{#each ticketDrafts as t, i (i)}
			<div class="grid grid-cols-1 items-end gap-3 md:grid-cols-12">
				<div class="md:col-span-6">
					<label class="mb-1 block text-sm font-medium text-gray-700" for={`ticket-name-${i}`}>Name</label>
					<input
						id={`ticket-name-${i}`}
						class="input input-bordered w-full"
						placeholder="e.g. VIP"
						value={t.name}
						disabled={disabled}
						oninput={(e) => {
							const value = (e.target as HTMLInputElement).value;
							ticketDrafts = ticketDrafts.map((x, idx) => (idx === i ? { ...x, name: value } : x));
						}}
					/>
				</div>

				<div class="md:col-span-2">
					<label class="mb-1 block text-sm font-medium text-gray-700" for={`ticket-total-${i}`}>Total</label>
					<input
						id={`ticket-total-${i}`}
						class="input input-bordered w-full"
						type="number"
						min="1"
						step="1"
						value={t.total}
						disabled={disabled}
						oninput={(e) => {
							const value = Number((e.target as HTMLInputElement).value);
							ticketDrafts = ticketDrafts.map((x, idx) =>
								idx === i ? { ...x, total: Number.isFinite(value) ? value : 0 } : x
							);
						}}
					/>
				</div>

				<div class="md:col-span-2">
					<label class="mb-1 block text-sm font-medium text-gray-700" for={`ticket-price-${i}`}>Price</label>
					<input
						id={`ticket-price-${i}`}
						class="input input-bordered w-full"
						type="number"
						min="0"
						step="1"
						value={t.price}
						disabled={disabled}
						oninput={(e) => {
							const value = Number((e.target as HTMLInputElement).value);
							ticketDrafts = ticketDrafts.map((x, idx) =>
								idx === i ? { ...x, price: Number.isFinite(value) ? value : 0 } : x
							);
						}}
					/>
				</div>

				<div class="md:col-span-2 flex justify-end">
					<button type="button" class="btn btn-sm btn-ghost text-error" onclick={() => removeTicketDraft(i)} disabled={disabled}>
						Remove
					</button>
				</div>
			</div>
		{/each}
	</div>
</div>
