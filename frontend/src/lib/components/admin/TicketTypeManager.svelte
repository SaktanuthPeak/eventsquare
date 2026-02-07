<script lang="ts">
	import type { TicketType } from '$lib/models/tickets';

	let { ticketTypes = [] as TicketType[] } = $props<{ ticketTypes?: TicketType[] }>();

</script>

<div class="mt-6 overflow-x-auto rounded-lg border border-base-300 bg-base-100">
	<table class="table">
		<thead>
			<tr>
				<th>Name</th>
				<th>Price</th>
				<th>Total</th>
				<th>Remaining</th>
			</tr>
		</thead>
		<tbody>
			{#if ticketTypes.length === 0}
				<tr>
					<td colspan="4" class="py-10 text-center text-base-content/70">No ticket types yet.</td>
				</tr>
			{:else}
				{#each ticketTypes as t (t.ticket_id ?? t.name)}
					<tr>
						<td class="min-w-52">{t.name}</td>
						<td>{t.price}</td>
						<td>{t.total}</td>
						<td>{t.remaining ?? '-'}</td>
					</tr>
				{/each}
			{/if}
		</tbody>
	</table>
</div>
