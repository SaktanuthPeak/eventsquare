<script lang="ts">
	import { Toaster } from 'svelte-sonner';
	import Footer from '$lib/components/footer/footer.svelte';
	import LoginModal from './account/login/+page.svelte';
	import SignupModal from './register/+page.svelte';
	import '../app.css';
	import Navbar from '$lib/components/navbar/navbar.svelte';
	import type { PageData } from './$types';
	type Props = {
		data: PageData;
		children: () => any;
		showLoginModal: boolean;
		showSignupModal: boolean;
	};
	let {
		data,
		children,
		showLoginModal = $bindable(),
		showSignupModal = $bindable()
	}: Props = $props();
</script>

<div class="w-full overflow-x-hidden scroll-smooth min-h-screen hidescroll">
	<Navbar userData={data} />
	<Toaster richColors position="top-center" />
	<div class="min-h-screen">
		{@render children()}
	</div>
	<Footer />
	<LoginModal bind:showLoginModal />
	<SignupModal bind:showSignupModal />
</div>
