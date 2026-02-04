<script lang="ts">
	import { cn } from '$lib/utils/tw-utils';
	import { formatDateTime } from '$lib/utils/date-utils';
	import { Calendar, Receipt } from 'phosphor-svelte';

	let { order } = $props();

	function getStatusBgColor(status: string) {
		switch (status) {
			case 'completed':
				return 'bg-gradient-to-tl from-success/10 to-45% to-white';
			case 'pending':
				return 'bg-gradient-to-tl from-warning/10 to-45% to-white';
			case 'not_paid':
				return 'bg-gradient-to-tl from-error/10 to-45% to-white';
			case 'cancelled':
				return 'bg-gradient-to-tl from-error/10 to-45% to-white';
			default:
				return 'bg-white';
		}
	}

	function getStatusBadgeClass(status: string) {
		switch (status) {
			case 'completed':
				return 'badge badge-success';
			case 'pending':
				return 'badge badge-warning';
			case 'not_paid':
				return 'badge badge-error';
			case 'cancelled':
				return 'badge badge-error';
			default:
				return 'badge badge-neutral';
		}
	}
</script>

<div class={cn('card shadow-md h-fit ', getStatusBgColor(order?.order_status))}>
	<div
		class={cn(
			'card-body p-4 flex flex-col gap-1  rounded-xl',
			getStatusBgColor(order?.order_status)
		)}
	>
		<!-- Update the order header section -->
		<div class="flex flex-col sm:flex-row sm:justify-between items-start gap-2">
			<div class="w-full sm:w-auto">
				<h2 class="card-title text-lg truncate">Order #{order.order_number}</h2>
				<p class="text-sm text-base-content/70 truncate">
					{order.event_name || 'Unknown Event'}
				</p>
			</div>
			<div class="flex items-center gap-1 whitespace-nowrap">
				<span class="text-sm">Status:</span>
				<div class={getStatusBadgeClass(order.order_status)}>
					{order.order_status === 'not_paid'
						? 'Not Paid'
						: order.order_status.charAt(0).toUpperCase() + order.order_status.slice(1)}
				</div>
			</div>
		</div>

		<div class="divider my-0.5"></div>

		<!-- Replace the grid section -->
		<div class="grid grid-cols-1 xs:grid-cols-2 gap-1 text-sm">
			<div class="flex items-center gap-2">
				<Receipt size={16} class="text-primary flex-shrink-0" />
				<span class="truncate">Amount: ฿{order.total_amount}</span>
			</div>
			<div class="flex items-center gap-2">
				<Calendar size={16} class="text-primary flex-shrink-0" />
				<span class="truncate">Date: {formatDateTime(order.created_date)}</span>
			</div>
		</div>

		<div class=" flex flex-row justify-between items-end">
			<div class="flex flex-col gap-1">
				<p class="text-sm font-medium">Ticket: {order.ticket_type_name || 'Unknown'}</p>
				<p class="text-sm">Quantity: {order.audience_per_ticket}</p>
			</div>
			{#if order.order_status === 'pending'}
				<div class="card-actions items-end justify-end mt-2">
					<button class="btn btn-sm btn-primary">View Receipt</button>
				</div>
			{/if}
		</div>
	</div>
</div>
