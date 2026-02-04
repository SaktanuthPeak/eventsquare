<script lang="ts">
	import { X } from 'phosphor-svelte';
	import { goto } from '$app/navigation';
	import { toast } from 'svelte-sonner';
	import SuperDebug, { superForm } from 'sveltekit-superforms';
	import { signupSchema } from './schema';
	import { zodClient } from 'sveltekit-superforms/adapters';
	import TextInput from '$lib/components/ui/forms/TextInput.svelte';
	import type { PageData } from '../$types';

	let dialog = $state<HTMLDialogElement | null>(null);
	let error = $state('');

	type Props = {
		data?: PageData;
		showSignupModal?: boolean;
		returnUrl?: string;
	};
	let { data, showSignupModal = $bindable(), returnUrl }: Props = $props();

	const form = superForm(
		data?.form ?? {
			email: '',
			username: '',
			password: '',
			confirm_password: '',
			status: 'active',
			first_name: '',
			last_name: ''
		},
		{
			validators: zodClient(signupSchema),
			onResult: async ({ result }) => {
				if (result.type === 'success') {
					toast.success('Account created successfully!');
					showSignupModal = false;
					if (returnUrl) {
						await goto(returnUrl, { invalidateAll: true });
					} else {
						await goto('/');
					}
				} else {
					if (result.status === 409) {
						toast.error(result.data?.error ?? 'Username already exists.');
					} else {
						toast.error('An error occurred during signup.');
					}
				}
			}
		}
	);

	const { form: formData, errors, constraints, submitting, enhance } = form;
</script>

{#if showSignupModal}
	<div class="modal modal-open">
		<div class="modal-box z-[5000] bg-base-100 text-primary p-6">
			<!-- Header -->
			<div class="mb-3">
				<div class="flex justify-between items-center">
					<h3 class="font-bold text-lg">Sign Up to EventSquare</h3>
					<button
						type="button"
						class="btn btn-sm btn-circle btn-ghost"
						onclick={() => (showSignupModal = false)}
						aria-label="Close"
					>
						<X size={18} />
					</button>
				</div>
				<dd>Welcome our future organizer</dd>
			</div>

			{#if error}
				<div class="alert alert-error mb-4 text-sm">{error}</div>
			{/if}

			<!-- Use enhance action, so the form submission is handled by superForm -->
			<form method="POST" class="flex flex-col gap-4" action="/register" use:enhance>
				<div class="flex flex-row gap-3">
					<div class="form-control w-full">
						<TextInput
							{form}
							bind:value={$formData.first_name}
							name="first_name"
							label="First name"
							placeholder="Enter your first name"
							class="input input-bordered w-full"
						/>
					</div>
					<div class="form-control w-full">
						<TextInput
							{form}
							bind:value={$formData.last_name}
							name="last_name"
							label="Last name"
							placeholder="Enter your last name"
							class="input input-bordered w-full"
						/>
					</div>
				</div>

				<div class="form-control">
					<TextInput
						{form}
						bind:value={$formData.email}
						name="email"
						label="Email"
						placeholder="Enter your Email"
						class="input input-bordered w-full {$errors.email ? 'input-error' : ''}"
						{...$constraints.email}
					/>
				</div>

				<div class="form-control">
					<TextInput
						{form}
						bind:value={$formData.username}
						name="username"
						label="Username"
						placeholder="Enter your username"
						class="input input-bordered w-full {$errors.username ? 'input-error' : ''}"
						{...$constraints.username}
					/>
				</div>

				<div class="form-control">
					<TextInput
						{form}
						bind:value={$formData.password}
						name="password"
						type="password"
						label="Password"
						placeholder="Enter your password"
						class="input input-bordered w-full {$errors.password ? 'input-error' : ''}"
						{...$constraints.password}
					/>
				</div>

				<div class="form-control">
					<TextInput
						{form}
						bind:value={$formData.confirm_password}
						name="confirm_password"
						type="password"
						label="Confirm Password"
						placeholder="Confirm your password"
						class="input input-bordered w-full {$errors.confirm_password ? 'input-error' : ''}"
						{...$constraints.confirm_password}
					/>
				</div>

				<div class="form-control mt-2">
					<button type="submit" class="btn btn-primary w-full" disabled={$submitting}>
						{$submitting ? 'Signing up...' : 'Sign Up'}
					</button>
				</div>
			</form>
		</div>
	</div>
{/if}
