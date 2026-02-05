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
		validators: zodClient(userSchema),
		customValidity: true,
		onResult: async ({ result }) => {
			if (result?.type === 'success') {
				toast.success('เพิ่มผู้ใช้งานสำเร็จ');
				await goto(`/admin/users`, {
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

<div class="flex min-h-screen w-full flex-col items-center justify-center p-2 mt-12">
	<div
		class="card card-border border-base-content/5 rounded-4xl flex w-[55%] items-center justify-center bg-white p-4 shadow"
	><h1
				class="w-[180px] h-fit text-3xl font-extrabold cursor-pointer focus:outline-none focus:border-transparent focus:ring-0 border-0"
			>
				EventSquare
			</h1>
		<h1 class="text-2xl font-medium">Register / สมัครสมาชิก</h1>
		<form method="POST" use:enhance class="flex w-full flex-col gap-4 p-4">
			<div class="flex flex-col items-center justify-center gap-0.5">
				<div class="flex w-full gap-4">
					<div class="w-full">
						<TextInput
							{form}
							name="first_name"
							label="Name"
							type="text"
							placeholder="ชื่อ"
							class="input  w-full  rounded-md"
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
							class="input  w-full  rounded-md"
							bind:value={$formData.last_name}
						/>
					</div>
				</div>
				<div class="flex w-full gap-4">
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
				</div>
				<div class="flex w-full gap-2">
					<div class="w-full">
						<TextInput
							{form}
							name="email"
							label="Email"
							type="email"
							placeholder="อีเมล"
							class="input  w-full  rounded-md"
							bind:value={$formData.email}
						/>
					</div>
				</div>
				<div class="flex w-full gap-2">
					<div class="w-full">
						<TextInput
							{form}
							name="password"
							label="Password"
							type="password"
							placeholder="รหัสผ่าน"
							class="input  w-full  rounded-md"
							bind:value={$formData.password}
						/>
					</div>
				</div>
				<div class="flex w-full gap-2">
					<div class="w-full">
						<TextInput
							{form}
							name="confirm_password"
							label="Confirm Password"
							type="password"
							placeholder="ยืนยันรหัสผ่าน"
							class="input  w-full  rounded-md"
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

			<div class="flex items-center gap-2">
				<input
					type="checkbox"
					id="acceptTerms"
					onchange={() => (acceptTerms = !acceptTerms)}
					class="checkbox checkbox-primary"
				/>
				<span class=" text-sm">
					I accpet the <a href="/terms" target="_blank" class="text-primary"
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
			<div class="text-end text-sm text-gray-500">
				<a href="/account/login" class="text-primary hover:underline">
					มีบัญชีผู้ใช้แล้ว? เข้าสู่ระบบ
				</a>
			</div>

		</form>
	</div>
</div>