<script lang="ts">
	import { Check } from 'phosphor-svelte';
	import type { PageData } from './$types';
	import { superForm } from 'sveltekit-superforms';
	import QRCode from 'qrcode';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { toast } from 'svelte-sonner';

	export let data: PageData;

	let showSuccessModal: boolean = false;
	let successData: any = null;

	const { form, enhance, message, delayed, submitting } = superForm(data.form, {
		onResult: ({ result }) => {
			if (result.type === 'success' && result.data?.success) {
				showSuccessModal = true;
				successData = result.data?.returnData;
				
				setTimeout(() => {
					goto('/menu/check-in-history');
				}, 5000);
			} else if (result.type === 'failure') {
				toast.error(result.data?.error || 'Check-in failed');
			}
		}
	});

	let qrCodeUrl: string = '';
	let showQr: boolean = false;
	const generateQrCode = async () => {
		try {
			qrCodeUrl = await QRCode.toDataURL(data.ticket, {
				width: 300,
				margin: 2,
				color: {
					dark: '#000000',
					light: '#ffffff'
				}
			});
			showQr = true;
		} catch (err) {
			console.error('Error generating QR code', err);
			toast.error('Failed to generate QR code');
		}
	};

	onMount(() => {
		generateQrCode();
	});
</script>

<div class="container mx-auto max-w-md p-6 flex items-center justify-center min-h-screen">
	{#if showSuccessModal}
		<div class="fixed inset-0 flex items-center justify-center bg-black/50 z-50">
			<div class="bg-white rounded-xl shadow-2xl p-8 text-center animate-in fade-in zoom-in duration-300">
				<div class="flex justify-center mb-4">
					<div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center animate-bounce">
						<Check size={40} class="text-green-600" weight="bold" />
					</div>
				</div>
				<h2 class="text-2xl font-bold text-gray-800 mb-2">Check-in Successful!</h2>
				<p class="text-gray-600 mb-1">
					Welcome to <span class="font-semibold">{successData?.event_name}</span>
				</p>
				<p class="text-sm text-gray-500 mb-6">
					Redirecting to home page in 5 seconds...
				</p>
				<div class="w-full bg-gray-200 rounded-full h-1 overflow-hidden">
					<div class="bg-green-600 h-full animate-pulse" style="animation: countdown 5s linear forwards;"></div>
				</div>
			</div>
		</div>
	{:else}
		<div class="rounded-xl border bg-white shadow-lg w-full">
			<div class="border-b p-6 text-center">
				<h1 class="text-2xl font-bold text-gray-800">
					Event Check-in: {data.ticketData?.event?.name || 'Unknown Event'}
				</h1>
				<p class="text-sm text-gray-500">Event ID: {data.eventId}</p>
			</div>

			<div class="space-y-6 p-6">
				{#if data.ticketData}
					<div class="rounded-lg bg-gray-50 p-4">
						<h3 class="mb-2 font-semibold text-gray-700">
							{data.ticketData?.ticket_name || 'Unknown Ticket'} Details
						</h3>
						<div class="space-y-1 text-sm text-gray-600">
							<p><span class="font-medium">Ticket ID:</span> {data.ticket}</p>
							<p>
								<span class="font-medium">User:</span>
								{data.ticketData?.user?.first_name || 'Guest'}
								{data.ticketData?.user?.last_name || ''}
							</p>
							{#if data.ticketData.quantity}
								<p><span class="font-medium">Quantity:</span> {data.ticketData.quantity}</p>
							{/if}
							{#if data.ticketData.price_per_ticket}
								<p><span class="font-medium">Price:</span> ฿{data.ticketData.price_per_ticket}</p>
							{/if}
						</div>
					</div>
				{:else}
					<div class="rounded-lg bg-yellow-50 p-4 text-yellow-700">
						Loading ticket details or Ticket not found...
					</div>
				{/if}

				<hr />

				<!-- QR Code Section -->
				<div class="flex flex-col items-center justify-center space-y-4">
					{#if showQr && qrCodeUrl}
						<div class="flex flex-col items-center">
							<p class="text-sm font-medium text-center mb-3">Scan QR Code at Entrance</p>
							<div class="overflow-hidden rounded-lg border-4 border-indigo-100 shadow-sm">
								<img src={qrCodeUrl} alt="Ticket QR Code" class="h-64 w-64" />
							</div>
							<p class="mt-2 text-xs text-gray-400">Ticket ID: {data.ticket}</p>
						</div>
					{:else}
						<div class="flex items-center justify-center p-8 bg-base-200 rounded-lg h-64">
							<p class="text-sm text-gray-500">Generating QR code...</p>
						</div>
					{/if}
				</div>

				<hr />

				<!-- Check-in Form -->
				<form method="POST" use:enhance class="flex flex-col gap-4">
					<button
						type="submit"
						disabled={$submitting}
						class="w-full rounded-lg bg-indigo-600 px-4 py-3 font-semibold text-white transition hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed"
					>
						{#if $submitting}
							<span class="flex items-center justify-center gap-2">
								<svg class="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
									<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
									<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
								</svg>
								Checking in...
							</span>
						{:else}
							Confirm Check In
						{/if}
					</button>
				</form>

				{#if $message}
					<div class="rounded-lg bg-red-100 p-3 text-sm text-red-700">
						{$message}
					</div>
				{/if}
			</div>
		</div>
	{/if}
</div>

<style>
	@keyframes countdown {
		from {
			width: 100%;
		}
		to {
			width: 0%;
		}
	}
</style>