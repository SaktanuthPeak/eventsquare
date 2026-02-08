
<script lang="ts">
	import { superForm } from 'sveltekit-superforms';
	import type { PageData } from './$types';
	import { zodClient } from 'sveltekit-superforms/adapters';
	import { loginSchema } from '$lib/schemas/loginSchema';
	import TextInput from '$lib/components/ui/forms/TextInput.svelte';
	import { toast } from 'svelte-sonner';
	import { goto } from '$app/navigation';
	import type { ActionResult } from '@sveltejs/kit';

	export let data: PageData;

	const form = superForm(data.form, {
		validators: zodClient(loginSchema as any),
		onResult: async ({ result }) => {
			const resultData = (result as ActionResult & { data?: any })?.data;
			if (result.type === 'success' && resultData?.success === true) {
				toast.success('Successfully login');
				await goto('/', { invalidateAll: true });
			} else if (result.type === 'failure' && result.status === 400) {
				toast.error('ไม่สามารถเข้าสู่ระบบได้', {
					description: 'ข้อมูลที่ป้อนไม่ถูกต้อง กรุณาลองใหม่'
				});
			} else {
				toast.error('ไม่สามารถเข้าสู่ระบบได้', {
					description:
						resultData?.errors === 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง'
							? 'รหัสผ่านหรืออีเมลไม่ถูกต้อง'
							: 'กรุณาตรวจสอบข้อมูลของท่านและลองอีกครั้ง'
				});
			}
		}
	});
	const { form: formData, submitting, enhance } = form;
</script>

<div class="min-h-screen w-full bg-base-200 flex sm:py-14">
	<div class="mx-auto flex w-full max-w-md flex-col items-center py-8 justify-center">
		<div class="card card-border w-full border-base-content/10 bg-base-100 shadow-xl">
			<div class="card-body p-6 sm:p-8">
				<div class="flex flex-col gap-0.5">
					<h1 class="text-3xl font-extrabold leading-tight">EventSquare</h1>
					<p class="text-sm text-base-content/70">Login / เข้าสู่ระบบ</p>
				</div>

				<form method="post" use:enhance class="mt-6 flex w-full flex-col gap-3">
					<TextInput
						{form}
						bind:value={$formData.username}
						name="username"
						label="Username"
						placeholder="ชื่อผู้ใช้"
						autocomplete="username"
						autocapitalize="none"
						class="input w-full rounded-md"
					/>
					<TextInput
						{form}
						bind:value={$formData.password}
						type="password"
						name="password"
						label="Password"
						placeholder="รหัสผ่าน"
						autocomplete="current-password"
						class="input w-full rounded-md"
					/>

					<div class="flex items-center justify-between text-sm">
						<span class="text-base-content/60">Forgot password? (coming soon)</span>
						<a href="/account/signup" class="text-primary hover:underline">Create account</a>
					</div>

					<button
						type="submit"
						class="btn btn-primary mt-2 w-full"
						disabled={$submitting}
					>
						{$submitting ? 'กำลังเข้าสู่ระบบ...' : 'Login / เข้าสู่ระบบ'}
					</button>
				</form>
			</div>
		</div>
	</div>
</div>
