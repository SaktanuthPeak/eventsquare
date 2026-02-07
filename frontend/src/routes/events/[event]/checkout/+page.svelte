<script lang="ts">
	import type { PageData } from './$types';
	import { page } from '$app/state';
	import SuperDebug, { superForm, fileProxy } from 'sveltekit-superforms';
	import { zodClient } from 'sveltekit-superforms/adapters';
	import { checkoutSchema } from './schema';
	import TextInput from '$lib/components/ui/forms/TextInput.svelte';
	import FileInput from '$lib/components/ui/forms/FileInput.svelte';
	import FormErrorSummary from '$lib/components/ui/forms/FormErrorSummary.svelte';
	import type { AllEventInfo } from '$lib/client';
	import { getContext } from 'svelte';
	let { data }: { data: PageData } = $props();
	const ticketId = page.url.searchParams.get('ticketId');
	const ticketQuantities = page.url.searchParams.get('quantity');

	const form = superForm(data?.form, {
		validators: zodClient(checkoutSchema),
		onResult: ({ result }) => {
			if (result.type === 'success') {
				console.log('Form submitted successfully!!');
			} else {
				console.error('Form submission failed:');
			}
		},
		dataType: 'form'
	});

	const { form: formData, enhance, allErrors } = form;
	$formData.event_id = data?.eventData?.id || '';
	$formData.organizer_id = data?.eventData?.organizer_id || '';
	$formData.total_amount =
		(data?.eventData?.ticket_types?.find((ticket) => ticket.id === ticketId)?.price || 0) *
		(Number(ticketQuantities || 0) || 0);

	$formData.audience_per_ticket = Number(ticketQuantities) || 0;

	const file = fileProxy(form, 'slip_id');
</script>

<div class="px-[200px] py-[100px]">
	<form method="POST" enctype="multipart/form-data" use:enhance>
		<div class="flex flex-col px-30">
			<div>
				<TextInput
					{form}
					name="event_id"
					bind:value={$formData.event_id}
					type="hidden"
					hideErrors={true}
					required
				/>
				<TextInput
					{form}
					name="organizer_id"
					bind:value={$formData.organizer_id}
					type="hidden"
					required
				/>
				<TextInput
					{form}
					name="total_amount"
					bind:value={$formData.total_amount}
					type="hidden"
					hideErrors={true}
					required
				/>
				<TextInput
					{form}
					name="audience_per_ticket"
					bind:value={$formData.audience_per_ticket}
					type="hidden"
					hideErrors={true}
					required
				/>
			</div>
			<!-- Name -->
			<div class="flex w-full gap-4">
				<TextInput
					{form}
					name="owner_name"
					bind:value={$formData.owner_name}
					label="Owner Name"
					placeholder="Firstname Lastname"
					hideErrors={true}
					required
				/>
				<TextInput
					{form}
					name="co_owner_name"
					bind:value={$formData.co_owner_name}
					label="Co-Owner Name"
					placeholder="Firstname Lastname"
					hideErrors={true}
					required
				/>
			</div>

			<!-- Email -->
			<div class="flex w-full gap-4">
				<TextInput
					{form}
					name="owner_email"
					bind:value={$formData.owner_email}
					label="Owner Email"
					placeholder="Email"
					required
				/>
				<TextInput
					{form}
					name="co_owner_email"
					bind:value={$formData.co_owner_email}
					label="Co-Owner Email"
					placeholder="Email"
					hideErrors={true}
					required
				/>
			</div>

			<!-- Phone -->
			<div class="flex w-full gap-4">
				<TextInput
					{form}
					name="owner_phone"
					bind:value={$formData.owner_phone}
					label="Owner Phone"
					placeholder="Phone Number"
					hideErrors={true}
					required
				/>
				<TextInput
					{form}
					name="co_owner_phone"
					bind:value={$formData.co_owner_phone}
					label="Co-Owner Phone"
					placeholder="Phone Number"
					hideErrors={true}
					required
				/>
			</div>

			<div class="flex w-full gap-4">
				<FileInput
					{form}
					name="slip_id"
					bind:files={$file}
					label="Upload Slip"
					placeholder="Upload Owner ID"
					hideErrors={true}
					required
				/>
			</div>

			<div class="pt-4">
				<FormErrorSummary errors={$allErrors} />
			</div>
			<div>
				<button type="submit" class="btn btn-primary mt-4"> Submit </button>
			</div>
		</div>
	</form>
	<!-- <SuperDebug data={formData} /> -->
</div>
