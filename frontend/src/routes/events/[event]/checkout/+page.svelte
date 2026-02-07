<script lang="ts">
	import type { PageData } from './$types';
	import { page } from '$app/state';
	import { goto } from '$app/navigation';
	import { superForm } from 'sveltekit-superforms';
	import { zodClient } from 'sveltekit-superforms/adapters';
	import { checkoutSchema } from './schema';
	import FormErrorSummary from '$lib/components/ui/forms/FormErrorSummary.svelte';
	import { toast } from 'svelte-sonner';
	const props = $props<{ data: PageData }>();
	const ticketId = page.url.searchParams.get('ticketId');
	const quantityParam = page.url.searchParams.get('quantity');
	let purchaseCompleted = $state(false);

	const form = superForm(props.data?.form, {
		validators: zodClient(checkoutSchema as any),
		onResult: ({ result }) => {
			if (result.type === 'success') {
				purchaseCompleted = true;
				toast.success('Purchase completed', { description: 'Redirecting to My Tickets…' });
				setTimeout(() => {
					goto('/menu/my-tickets');
				}, 5000);
			} else {
				const message =
					result.type === 'failure'
						? ((result.data as any)?.message ?? 'Booking failed. Please try again.')
						: 'Booking failed. Please try again.';
				toast.error('Purchase failed', { description: message });
			}
		},
		dataType: 'json'
	});

	const { form: formData, enhance, allErrors, submitting } = form;
	$effect(() => {
		$formData.event_id = props.data?.eventData?.id || '';
		$formData.ticket_type_id = (props.data as any)?.selectedTicket?.id || ticketId || '';
		$formData.quantity = Number((props.data as any)?.form?.data?.quantity ?? quantityParam ?? 0);
	});

	const selectedTicketName = $derived.by(() => String((props.data as any)?.selectedTicket?.name ?? ''));
	const pricePerTicket = $derived.by(() => Number((props.data as any)?.selectedTicket?.price ?? 0));
	const totalPrice = $derived.by(() => pricePerTicket * Number($formData.quantity ?? 0));
</script>

<div class="bg-base-100">
	<div class="mx-auto max-w-6xl px-4 py-10">
		<div class="mb-6 flex flex-wrap items-center justify-between gap-3">
			<div class="breadcrumbs text-sm">
				<ul>
					<li><a href="/">Home</a></li>
					<li><a href={`/events/${props.data?.eventData?.id ?? ''}`}>Event</a></li>
					<li>Checkout</li>
				</ul>
			</div>
			<a class="btn btn-ghost btn-sm" href={`/events/${props.data?.eventData?.id ?? ''}`}>Back</a>
		</div>

		<div class="grid gap-6 lg:grid-cols-5">
			<div class="lg:col-span-3">
				<div class="card border border-base-300 bg-base-200/60">
					<div class="card-body gap-6">
						<div>
							<h1 class="text-2xl font-semibold">Checkout</h1>
							{#if props.data?.eventData}
								<p class="text-base-content/70">{props.data.eventData.name}</p>
							{/if}
						</div>

						{#if props.data?.image}
							<img
								src={`${props.data?.image}`}
								alt={props.data?.eventData?.name ?? 'Event image'}
								class="h-40 w-full rounded-box object-cover"
								loading="lazy"
							/>
						{/if}

						{#if purchaseCompleted}
							<div class="rounded-box border border-success/30 bg-success/10 p-6">
								<h2 class="text-lg font-semibold text-success">Purchase completed</h2>
								<p class="mt-1 text-sm text-base-content/70">
									Thanks! We’re redirecting you to My Tickets.
								</p>
								<div class="mt-4">
									<a class="btn btn-success btn-sm" href="/menu/my-tickets">Go now</a>
								</div>
							</div>
						{:else}
							<form method="POST" use:enhance class="space-y-5">
							<input type="hidden" name="event_id" bind:value={$formData.event_id} required />
							<input type="hidden" name="ticket_type_id" bind:value={$formData.ticket_type_id} required />
							<input type="hidden" name="quantity" bind:value={$formData.quantity} required />

							<div class="rounded-box border border-base-300 bg-base-100 p-4">
								<div class="grid gap-3 md:grid-cols-2">
									<div>
										<div class="text-xs text-base-content/60">Ticket type</div>
										<div class="font-medium">{selectedTicketName || '-'}</div>
									</div>
									<div>
										<div class="text-xs text-base-content/60">Quantity</div>
										<div class="font-medium">{Number($formData.quantity ?? 0)}</div>
									</div>
								</div>
								<p class="mt-3 text-xs text-base-content/60">
									Selection is locked from the event page.
								</p>
							</div>

							<div>
								<FormErrorSummary errors={$allErrors} />
							</div>

							<div class="card-actions justify-end">
								<button
									type="submit"
									class={`btn btn-primary ${$submitting ? 'btn-disabled' : ''}`}
									disabled={$submitting}
								>
									{#if $submitting}
										<span class="loading loading-spinner loading-sm"></span>
										Booking...
									{:else}
										Book tickets
									{/if}
								</button>
							</div>
						</form>
					{/if}
					</div>
				</div>
			</div>

			<div class="lg:col-span-2">
				<div class="card sticky top-6 border border-base-300 bg-base-200/60">
					<div class="card-body">
						<h2 class="card-title">Order summary</h2>
							<div class="divider my-2"></div>

						<div class="flex items-center justify-between gap-4">
							<span class="text-base-content/70">Ticket</span>
							<span class="font-medium text-right">{selectedTicketName || '-'}</span>
						</div>
						<div class="flex items-center justify-between gap-4">
							<span class="text-base-content/70">Price</span>
							<span>{pricePerTicket}</span>
						</div>
						<div class="flex items-center justify-between gap-4">
							<span class="text-base-content/70">Quantity</span>
							<span>{Number($formData.quantity ?? 0)}</span>
						</div>

							<div class="divider my-2"></div>
						<div class="flex items-center justify-between gap-4 text-lg font-semibold">
							<span>Total</span>
							<span>{totalPrice}</span>
						</div>
						<p class="mt-2 text-xs text-base-content/60">
							Total is calculated from current ticket price × quantity.
						</p>
					</div>
				</div>
			</div>
		</div>
	</div>
</div>
