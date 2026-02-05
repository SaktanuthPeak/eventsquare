
<script lang="ts">
	import { superForm } from 'sveltekit-superforms';
	import type { PageData } from './$types';
	import { zodClient } from 'sveltekit-superforms/adapters';
	import { loginSchema } from '$lib/schemas/loginSchema';
	import TextInput from '$lib/components/ui/forms/TextInput.svelte';
	import { toast } from 'svelte-sonner';
	import { goto } from '$app/navigation';

	let { data }: { data: PageData } = $props();
	let loading = $state(false);

	const form = superForm(data.form, {
		validators: zodClient(loginSchema),
		onResult: async ({ result }) => {
			if (result?.data?.success === true) {
				toast.success('Successfully login');
				await goto('/', { invalidateAll: true });
			} else if (result.status === 400) {
				toast.error('ไม่สามารถเข้าสู่ระบบได้', {
					description: 'ข้อมูลที่ป้อนไม่ถูกต้อง กรุณาลองใหม่'
				});
			} else {
				toast.error('ไม่สามารถเข้าสู่ระบบได้', {
					description:
						result.data?.errors === 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง'
							? 'รหัสผ่านหรืออีเมลไม่ถูกต้อง'
							: 'กรุณาตรวจสอบข้อมูลของท่านและลองอีกครั้ง'
				});
			}
		}
	});
	const { form: formData, enhance } = form;
</script>

<div class="flex h-screen w-full flex-col items-center justify-center">
	<div class="card card-border border-base-content/5 rounded-4xl mt-10 bg-white min-w-md p-4 shadow">
		<form method="post" use:enhance>
			<h1
				class="w-full h-fit text-3xl font-extrabold cursor-pointer focus:outline-none focus:border-transparent focus:ring-0 border-0"
			>
				EventSquare
			</h1>
			<div class="card-body">
				<h2 class="card-title flexx justify-center text-2xl">Member login</h2>
				<TextInput
					{form}
					bind:value={$formData.username}
					name="username"
					label="Username"
					placeholder="ชื่อผู้ใช้"
				/>
				<TextInput
					{form}
					bind:value={$formData.password}
					type="password"
					name="password"
					label="Password"
					placeholder="รหัสผ่าน"
				/>
				<a href="/account/forgot-password">Forgot password?</a>
				<div class="card-action justify-end">
					<button type="submit" class="btn btn-primary w-full" disabled={loading}>
						{loading ? 'กำลังเข้าสู่ระบบ...' : 'Login/เข้าสู่ระบบ'}
					</button>
				</div>
				<a href="/account/register" class="text-center underline">Sign Up/สมัครเข้าใช้งาน</a>
			</div>
			<!-- <SuperDebug data={$formData} /> -->
		</form>
	</div>
</div>
