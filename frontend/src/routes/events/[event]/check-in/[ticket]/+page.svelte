<script lang="ts">
	import { Check } from 'phosphor-svelte';
	import type { PageData } from './$types';
	import SuperDebug, { superForm } from 'sveltekit-superforms';
	import { zodClient } from 'sveltekit-superforms/adapters';
	import { checkInSchema } from './schema';
	import TextInput from '$lib/components/ui/forms/TextInput.svelte';
	import { toast } from 'svelte-sonner';
	import { page } from '$app/state';
	import { goto } from '$app/navigation';
	import { generateQRCode } from '$lib/utils/qrcode';
	import { onMount } from 'svelte';

	let { data }: { data: PageData } = $props();
	let showCheckInModal: boolean = $state(false);
	let qrCodeUrl: string = $state('');
	let returnUrl = $derived(page.url.pathname);
	let returnEventData = $state<Object[]>([]);

	onMount(async () => {
		// Generate QR code from ticket ID
		if (data.ticket) {
			try {
				qrCodeUrl = await generateQRCode(data.ticket);
			} catch (err) {
				console.error('Failed to generate QR code:', err);
				toast.error('Failed to generate QR code');
			}
		}
	});

	const form = superForm(data.form, {
		validators: zodClient(checkInSchema),
		onResult: ({ result }) => {
			if (result.type === 'success') {
				toast.success('You Welcome to the event');
				returnEventData = result.data?.returnData;
				showCheckInModal = true;
			} else if (result.type === 'failure') {
				if (result.status === 401) {
					toast.error('Check-in failed,Please Login before check-in');
				} else {
					toast.error(result.data?.error ?? 'Unknown error occurred during check-in');
				}
			}
		}
	});
	const { form: formData, enhance, allErrors } = form;

	$formData.eventId = data.eventId.event;

</script>

{#if showCheckInModal}
	<div class="modal modal-open">
		<div class="modal-box flex flex-col items-center gap-4">
			<Check size={48} class="text-green-500" />
			<h1 class="text-2xl font-bold">Check-in Successful!</h1>
			<div class="text-lg">
				Welcome to <span class="font-semibold">{returnEventData?.event_name}</span>
			</div>

			<button class="btn btn-primary mt-4" onclick={() => goto('/')}>Close</button>
		</div>
	</div>
{:else}
	<div class="modal modal-open">
		<div class="modal-box w-full max-w-md">
			<h2 class="text-xl font-semibold mb-2">Event Check-in</h2>
			<p class="mb-4 text-gray-600">
				By checking in, you agree to give consent for participating in the event.
				<button
					class="text-blue-500 cursor-pointer hover:underline"
					onclick={() => goto('/account/login', { replaceState: true, invalidateAll: true })}
				>
					policy & term of service
				</button>
			</p>

			<!-- QR Code Section -->
			{#if qrCodeUrl}
				<div class="flex flex-col items-center gap-3 mb-6 p-4 bg-base-100 rounded-lg border-2 border-dashed border-primary">
					<p class="text-sm font-medium text-center">Scan QR Code to Check In</p>
					<img src={qrCodeUrl} alt="QR Code for check-in" class="w-48 h-48 rounded-lg" />
					<p class="text-xs text-gray-500 text-center">Ticket ID: {data.ticket}</p>
				</div>
			{:else}
				<div class="flex items-center justify-center mb-6 p-4 bg-base-200 rounded-lg h-56">
					<p class="text-sm text-gray-500">Loading QR code...</p>
				</div>
			{/if}

			<!-- Check-in Button Section -->
			<form method="POST" use:enhance class="flex flex-col gap-4">
				<TextInput {form} bind:value={$formData.eventId} name="eventId" type="hidden" />
				
				<!-- Ticket Information (if available) -->
				{#if data.ticketData}
					<div class="bg-blue-50 p-3 rounded-lg text-sm">
						<p class="font-medium text-blue-900 mb-1">{data.ticketData.ticket_name}</p>
						<p class="text-blue-700">Qty: {data.ticketData.quantity}</p>
						<p class="text-blue-700">Price: ฿{data.ticketData.price_per_ticket}</p>
					</div>
				{/if}

				<button class="btn btn-primary" type="submit">Confirm Check In</button>
			</form>

			{#if $allErrors.length}
				<ul class="mt-2 text-error text-sm">
					{#each $allErrors as err}
						<li>{err.messages.join(', ')}</li>
					{/each}
				</ul>
			{/if}
		</div>
	</div>
{/if}

