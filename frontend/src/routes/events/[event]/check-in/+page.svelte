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

	let { data }: { data: PageData } = $props();
	let showCheckInModal: boolean = $state(false);
	let returnUrl = $derived(page.url.pathname);
	let returnEventData = $state<Object[]>([]);

	const form = superForm(data.form, {
		validators: zodClient(checkInSchema),
		onResult: ({ result }) => {
			if (result.type === 'success') {
				toast.success('You Welcome to the event');
				returnEventData = result.data?.returnData;
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
		<div class="modal-box">
			<h2 class="text-xl font-semibold mb-2">Event Check-in</h2>
			<p class="mb-4 text-gray-600">
				By checking in, you agree to give consent for participating in the event.
				<button
					class="text-blue-500 cursor-pointer hover:underline"
					onclick={() => goto('/account/login', { replaceState: true, invalidateAll: true })}
				>
					prolicy & term of service
				</button>
			</p>
			<form method="POST" use:enhance class="flex flex-col gap-4">
				<TextInput {form} bind:value={$formData.eventId} name="eventId" type="hidden" />
				<button class="btn btn-primary" type="submit">Check In</button>
			</form>
			{#if $allErrors.length}
				<ul class="mt-2 text-error text-sm">
					{#each $allErrors as err}
						<li>{err.messages.join(', ')}</li>
					{/each}
				</ul>
			{/if}
			<!-- <SuperDebug data={formData} /> -->
		</div>
	</div>
{/if}

