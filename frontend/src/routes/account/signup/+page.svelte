<script lang="ts">
	import { goto } from '$app/navigation';
	import { toast } from 'svelte-sonner';
	import type { PageData } from './$types';
	import SuperDebug, { superForm } from 'sveltekit-superforms';
	import { zodClient } from 'sveltekit-superforms/adapters';
	import TextInput from '$lib/components/ui/forms/TextInput.svelte';
	import { userSchema } from '$lib/schemas/userSchema';
	import { XCircle } from 'phosphor-svelte';

	let { data }: { data: PageData } = $props();
	let acceptTerms = $state(false);

	const form = superForm(data?.form, {
		validators: zodClient(userSchema as any),
		customValidity: true,
		onResult: async ({ result }) => {
			if (result?.type === 'success') {
				toast.success('เพิ่มผู้ใช้งานสำเร็จ');
				await goto(`/`, {
					invalidateAll: true
				});
			} else if (result?.type === 'failure') {
				toast.error(`Error: ${result?.data?.status} ไม่สามารถเพิ่มผู้ใช้งานได้`, {
					description: result.data?.message || 'กรุณาตรวจสอบข้อมูลและลองอีกครั้ง'
				});
			} else {
				toast.error('มีบางอย่างผิดพลาด กรุณาลองใหม่อีกครั้ง');
			}
		},
		dataType: 'json'
	});

	const { form: formData, allErrors, submitting, enhance } = form;
</script>

<div class="min-h-screen w-full px-4 py-10 sm:py-12">
	<div class="mx-auto flex w-full max-w-2xl flex-col items-center justify-center">
		<div class="card card-border w-full border-base-content/5 bg-white shadow">
			<div class="card-body p-5 sm:p-8">
				<div class="flex flex-col gap-2 sm:flex-row sm:items-end sm:justify-between">
					<h1 class="text-3xl font-extrabold leading-tight">EventSquare</h1>
					<h2 class="text-lg font-medium sm:text-right">Register / สมัครสมาชิก</h2>
				</div>

				<form method="POST" use:enhance class="mt-4 flex w-full flex-col gap-4">
					<div class="flex flex-col gap-4">
						<div class="flex w-full flex-col gap-4 md:flex-row">
							<div class="w-full">
								<TextInput
									{form}
									name="first_name"
									label="Name"
									type="text"
									placeholder="ชื่อ"
									class="input w-full rounded-md"
									bind:value={$formData.first_name}
								/>
							</div>
							<div class="w-full">
								<TextInput
									{form}
									name="last_name"
									label="Surname"
									type="text"
									placeholder="นามสกุล"
									class="input w-full rounded-md"
									bind:value={$formData.last_name}
								/>
							</div>
						</div>

						<div class="w-full">
							<TextInput
								{form}
								name="username"
								label="Username"
								type="text"
								placeholder="ชื่อผู้ใช้"
								class="input w-full rounded-md"
								bind:value={$formData.username}
								onchange={() => {
									$formData.email = $formData.username + '@gmail.com';
								}}
							/>
						</div>

						<div class="w-full">
							<TextInput
								{form}
								name="email"
								label="Email"
								type="email"
								placeholder="อีเมล"
								class="input w-full rounded-md"
								bind:value={$formData.email}
							/>
						</div>

						<div class="flex w-full flex-col gap-4 md:flex-row">
							<div class="w-full">
								<TextInput
									{form}
									name="password"
									label="Password"
									type="password"
									placeholder="รหัสผ่าน"
									class="input w-full rounded-md"
									bind:value={$formData.password}
								/>
							</div>
							<div class="w-full">
								<TextInput
									{form}
									name="confirm_password"
									label="Confirm Password"
									type="password"
									placeholder="ยืนยันรหัสผ่าน"
									class="input w-full rounded-md"
									bind:value={$formData.confirm_password}
								/>
							</div>
						</div>
					</div>
			{#if $allErrors.length}
				<div class="rounded-lg border border-red-100 bg-red-50 p-4">
					<div class="flex">
						<div class="flex-shrink-0">
							<XCircle size={22} weight="fill" class="text-red-500" />
						</div>
						<div class="ml-1">
							<h3 class="text-sm font-medium text-red-800">
								Please fix the following {$allErrors.length === 1 ? 'error' : 'errors'}:
							</h3>
							<div class="mt-2 text-sm text-red-700">
								<ul class="list-disc space-y-1 pl-5">
									{#each $allErrors as error}
										<li>
											{#if error.path.includes('checkInRange')}
												Check-in range: {error.messages.join('. ')}
											{:else if error.path[0] === '_errors'}{error.messages.join('. ')}
											{:else}
												{error.messages.join('. ')}
											{/if}
										</li>
									{/each}
								</ul>
							</div>
						</div>
					</div>
				</div>
			{/if}

			<div class="flex items-start gap-3">
				<input
					type="checkbox"
					id="acceptTerms"
					onchange={() => (acceptTerms = !acceptTerms)}
					class="checkbox checkbox-primary"
				/>
				<span class="text-sm leading-snug">
					I accept the <a href="/terms" target="_blank" class="text-primary"
						>Terms and Conditions.</a
					>
				</span>
			</div>
			<div class="form-control flex w-full justify-between">
				<button
					class="btn bg-primary w-full rounded-md text-white"
					type="submit"
					disabled={$submitting || acceptTerms === false}
				>
					{$submitting ? 'กำลังบันทึก...' : 'สมัครสมาชิก'}
				</button>
			</div>
			<div class="text-center text-sm text-gray-500 sm:text-end">
				<a href="/account/login" class="text-primary hover:underline">
					มีบัญชีผู้ใช้แล้ว? เข้าสู่ระบบ
				</a>
			</div>
				</form>
			</div>
		</div>
	</div>
</div>