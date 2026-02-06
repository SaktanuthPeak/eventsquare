<script lang="ts">
	import { cn } from '$lib/utils/tw-utils';
	import { User, Calendar, BookBookmark } from 'phosphor-svelte';
	import { formatAllowedDates } from '$lib/utils/allowed-date-utils';
	let { ticket } = $props();
</script>
<!-- Ph.bookBookmark.regular
    .frame(width: 32, height: 32) -->
    
<div
	class="card w-full bg-gradient-to-tr from-pink-100 to-40% hover:shadow-lg transition-all border border-base-200"
>
	<div class="flex flex-col sm:flex-row">
		<!-- Ticket Details -->
		<div class="p-4 flex flex-col gap-1 w-full">
			<div class="flex justify-between items-center">
				<h2 class="card-title text-lg font-bold truncate w-[60%]">
					{ticket?.event?.name || '**Event Name**'}
				</h2>
				<div class="badge badge-primary">
					{ticket.status?.charAt(0).toUpperCase() + ticket.status?.slice(1)}
				</div>
			</div>

			<div class=" space-y-1">
				<div class="flex items-center gap-2">
					<User size={18} class="text-primary/60" />
 					<span class="text-sm">Owner: {`${ticket?.user?.first_name || 'Unknown'} ${ticket?.user?.last_name || ''}`}</span>
				</div>


				<div class="flex items-center gap-2">
					<Calendar size={18} class="text-primary/60" />
					<span class="text-sm">
						{formatAllowedDates({
							date_range: {
								start_date: ticket?.event_start_date || "Wed Feb 04 2026 14:44:24 GMT+0700 (Indochina Time)",
								end_date: ticket?.event_end_date || "Wed Feb 10 2026 18:00:00 GMT+0700 (Indochina Time)"
							}
						})}
					</span>
				</div>

				<div class="flex items-center gap-2">
					<BookBookmark size={18} class="text-primary/60" />
					<span class="text-sm">check-in: {ticket?.is_checked_in ? 'Checked In' : 'Not Checked In'}</span>
				</div>
			</div>

			<div class="divider my-1"></div>

			<div class="flex justify-between">
				<div>
					<p class="text-sm font-medium">Ticket Type:</p>
					<p class="text-primary font-semibold">
						{ticket?.ticket_name || 'General Admission'}
					</p>
				</div>
				<div>
					<p class="text-sm font-medium">Quantity:</p>
					<p class="text-primary items-center justify-center font-semibold">{ticket?.quantity}</p>
				</div>
			</div>

			<div class="card-actions justify-between md:gap-2 mt-2">
				<a href={`/events/${ticket?.event?.id || ''}`} class="btn btn-sm btn-primary flex-1">
					View Event
				</a>
				{#if ticket?.is_checked_in}
					<button class="btn btn-sm btn-success flex-1" style="background-color: #ffcccc;" disabled>
						✓ Checked In
					</button>
				{:else}
					<a href={`/events/${ticket?.event?.id}/check-in/${ticket?.id}`} class="btn btn-sm btn-secondary flex-1">
						Check-in
					</a>
				{/if}
			</div>
			
		</div>
	</div>
</div>
