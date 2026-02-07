<script lang="ts">
	import { superForm } from 'sveltekit-superforms';
	import type { PageData } from './$types';
	import { goto } from '$app/navigation';
	import { toast } from 'svelte-sonner';
	import { Calendar, Ticket, Info, Warning } from 'phosphor-svelte';
	import EventDetailsCard from '$lib/components/cards/EventCardDetails.svelte';
	import MobileEventDetailsCard from '$lib/components/cards/EventCardDetailsMobile.svelte';
	import { cn } from '$lib/utils/tw-utils';
	import { fade, fly } from 'svelte/transition';
	import { env } from '$env/dynamic/public';

	let { data }: { data: PageData } = $props();
	let selectedTicketType: string = $state('');
	let ticketQuantities: Record<string, number> = $state({});
	let submitStatus = $state(false);
	let agreedToTerms = $state(false);

	function handleSelectTicket(selectedTicketType: any) {
		if (!selectedTicketType) {
			toast.error('Please select a ticket type.');
			return;
		}
		if (!agreedToTerms) {
			toast.error('Please accept the terms of service.');
			return;
		}
		const quantity = Number(ticketQuantities[selectedTicketType] ?? 0);
		if (!Number.isFinite(quantity) || quantity <= 0) {
			toast.error('Please select a valid quantity.');
			return;
		}
		submitStatus = true;
		goto(
			`/events/${data?.eventData?.id}/checkout?ticketId=${encodeURIComponent(
				String(selectedTicketType)
			)}&quantity=${encodeURIComponent(String(quantity))}`
		);
	}
	$effect(() => {
		if (selectedTicketType && !ticketQuantities[selectedTicketType]) {
			ticketQuantities[selectedTicketType] = 1;
		}
	});
</script>

<div class="flex flex-col items-center w-full">
	<!-- Hero Banner Section -->
	<div class="w-full h-[60vh] relative">
		{#if data.eventData?.image_id}
			<div class="absolute inset-0 overflow-hidden">
				<img
					class="w-full h-full object-cover"
					src={`${env.PUBLIC_API_URL}/v1/images/${data.eventData.image_id}`}
					alt={data.eventData?.name}
					transition:fade={{ duration: 300 }}
				/>
				<div class="absolute inset-0 bg-linear-to-b from-black/60 to-transparent"></div>
			</div>
		{:else}
			<div
				class="absolute inset-0 bg-linear-to-br from-primary/10 to-secondary/10 flex items-center justify-center"
			>
				<div class="text-center p-8 rounded-xl">
					<Warning size={64} weight="light" class="mx-auto text-primary/30 mb-4" />
					<h2 class="text-xl font-medium text-primary/70">No Event Banner Available</h2>
				</div>
			</div>
		{/if}

		<!-- Event Title Overlay -->
		<div
			class="hidden md:block absolute bottom-0 left-0 w-full p-8 bg-linear-to-t from-black/50 to-transparent text-white"
		>
			<div class="container mx-auto">
				<h1 class="text-3xl md:text-4xl font-bold mb-2" transition:fly={{ y: 20, duration: 400 }}>
					{data.eventData?.name}
				</h1>
				<div class="flex flex-wrap gap-3 items-center">
					<div class="badge badge-accent">{(data.eventData as any)?.event_type || 'Event'}</div>
					<div
						class={cn(
							'badge ',
							data.eventData?.event_type === 'public' ? 'badge-success' : 'badge-secondary'
						)}
					>
						{data.eventData?.event_type === 'public' ? 'Public' : 'Private'}
					</div>
				</div>
			</div>
		</div>
	</div>

	<!-- Mobile Event Details -->

	<!-- Main Content Area -->
	<div class="container mx-auto px-4 py-8 flex flex-col-reverse lg:flex-row gap-8">
		<!-- Left Column: Event Details -->
		<div class="w-full relative bottom-117.5 md:bottom-0 lg:w-5/7 space-y-8">
			<!-- Desktop Event Details Card -->
			<div class=" md:hidden w-full">
				<MobileEventDetailsCard eventData={data.eventData} />
			</div>

			<!-- Event Description -->
			<div class="bg-white rounded-xl shadow-sm border border-base-200 p-6">
				<h2 class="font-bold text-2xl flex items-center gap-2 mb-4">
					<Info size={24} class="text-primary/70" />
					Event Description
				</h2>
				<div class="prose max-w-none mt-4 whitespace-pre-line">
					{data.eventData?.description || 'No description available.'}
				</div>
			</div>

		</div>

		<div class={cn('w-full lg:w-2/7 hidden lg:block')}>
			<div class="relative bottom-85">
				<EventDetailsCard eventData={data?.eventData} />
			</div>
			<div
				class={cn(
					'relative bottom-80 ',
					data?.eventData?.event_type === 'public' ? 'hidden' : ''
				)}
			>
				<div class="rounded-xl overflow-hidden bg-white border border-base-200 shadow-lg">
					<!-- Ticket Header -->
					<div class="bg-primary text-primary-content p-4">
						<h2 class="text-xl font-bold flex items-center text-white gap-2">
							<Ticket size={24} weight="bold" />
							Event Tickets
						</h2>
					</div>

					<!-- Ticket List -->
					<div class="divide-y">
						{#if data?.eventData?.ticket_types && data?.eventData.ticket_types.length > 0}
							{#each data?.eventData?.ticket_types as ticket}
								<div class="p-4 hover:bg-base-100 transition-colors">
									<div class="flex justify-between items-start">
										<div class="space-y-1">
											<h3 class="font-bold text-lg">{ticket?.name}</h3>
											<p class="text-sm text-base-content/70">{(ticket as any)?.description}</p>

											{#if (ticket as any)?.allowed_dates}
												<div class="mt-2 flex items-center gap-1 text-xs text-primary/60">
													<Calendar size={14} />
													<span>
														{#if (ticket as any)?.allowed_dates?.date_range}
															{new Date(
																(ticket as any)?.allowed_dates?.date_range?.start_date
															).toLocaleDateString()} -
															{new Date(
																(ticket as any)?.allowed_dates?.date_range?.end_date
															).toLocaleDateString()}
														{:else if (ticket as any)?.allowed_dates?.single_date}
															{new Date((ticket as any)?.allowed_dates?.single_date).toLocaleDateString()}
														{/if}
													</span>
												</div>
											{/if}
										</div>
										<div class="font-bold text-xl text-secondary">฿{ticket.price}</div>
									</div>
								</div>
							{/each}
						{:else}
							<div class="p-8 text-center text-base-content/70">
								<Warning size={40} weight="light" class="mx-auto mb-2" />
								<p>No tickets available for this event</p>
							</div>
						{/if}
					</div>

					<!-- Purchase Form -->
					<div class="p-4 bg-base-100 space-y-4">
						<div class="form-control">
							<select class="select select-bordered w-full" bind:value={selectedTicketType}>
								<option value="" disabled selected>Choose a ticket type</option>
								{#each data?.eventData?.ticket_types || [] as ticket}
								{#if (ticket as any)?.remaining > 0}
									<option value={(ticket as any)?.id ?? (ticket as any)?.ticket_id} >{ticket?.name} - ฿{ticket?.price}</option>
								{:else}
									<option value={(ticket as any)?.id ?? (ticket as any)?.ticket_id} disabled>
										{ticket?.name} - Sold Out
									</option>
								{/if}
								{/each}
							</select>
						</div>

						{#if selectedTicketType}
							<div class="form-control">
								<label class="label" for="ticket-quantity">
									<span class="label-text">Quantity</span>
								</label>
								<input
									id="ticket-quantity"
									type="number"
									min="1"
									max="10"
									class="input input-bordered w-full"
									bind:value={ticketQuantities[selectedTicketType]}
								/>
							</div>
						{/if}

						<div class="form-control">
							<label class="label cursor-pointer justify-start gap-2">
								<input
									type="checkbox"
									class="checkbox checkbox-primary"
									bind:checked={agreedToTerms}
								/>
								<span class="label-text"
									>I accept the <a href="/term_of_service" class="text-primary underline"
										>terms of service</a
									></span
								>
							</label>
						</div>

						<button
							class="btn btn-primary w-full"
							disabled={!selectedTicketType || !agreedToTerms}
							onclick={() => handleSelectTicket(selectedTicketType)}
						>
							Purchase Tickets
						</button>
					</div>
				</div>
			</div>
		</div>
	</div>
</div>
