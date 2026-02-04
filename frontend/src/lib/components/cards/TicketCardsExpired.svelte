<script lang="ts">
	import { cn } from '$lib/utils/tw-utils';
	import { User, UserCirclePlus, Calendar, MapPin } from 'phosphor-svelte';
	import { formatAllowedDates } from '$lib/utils/allowed-date-utils';
	let { ticket } = $props();
</script>

<div
	class="card w-full bg-gradient-to-tr from-base-200 hover:shadow-lg transition-all border border-base-200"
>
	<div class="flex flex-col sm:flex-row">
		<!-- Ticket Details -->
		<div class="p-4 flex flex-col gap-1 w-full">
			<div class="flex justify-between items-center">
				<h2 class="card-title text-lg font-bold truncate w-[60%]">
					{ticket?.event_name || '**Event Name**'}
				</h2>
				<div class="badge badge-error">Expired</div>
			</div>

			<div class=" space-y-1">
				<div class="flex items-center gap-2">
					<User size={18} class="text-primary/60" />
					<span class="text-sm">Owner: {ticket?.owner_name || 'Ticket Owner'}</span>
				</div>

				<div class="flex items-center gap-2">
					<UserCirclePlus size={18} class="text-primary/60" />
					<span class="text-sm">Co-owner: {ticket?.co_owner_name || 'Ticket Owner'}</span>
				</div>

				<div class="flex items-center gap-2">
					<Calendar size={18} class="text-primary/60" />
					<span class="text-sm">
						{formatAllowedDates(ticket?.allowed_dates) || 'Event Date'}
					</span>
				</div>

				<div class="flex items-center gap-2">
					<MapPin size={18} class="text-primary/60" />
					<span class="text-sm">{ticket?.location || 'Event Location'}</span>
				</div>
			</div>

			<div class="divider my-1"></div>

			<div class="flex justify-between">
				<div>
					<p class="text-sm font-medium">Ticket Type:</p>
					<p class="text-primary font-semibold">
						{ticket?.ticket_type_name || 'General Admission'}
					</p>
				</div>
				<div>
					<p class="text-sm font-medium">Quantity:</p>
					<p class="text-primary font-semibold">{ticket?.total_audience}</p>
				</div>
			</div>
		</div>
	</div>
</div>
