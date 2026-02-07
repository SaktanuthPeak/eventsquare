<script lang="ts">
	import { Toaster } from 'svelte-sonner';
	import Footer from '$lib/components/footer/footer.svelte';
	import '../app.css';
	import Navbar from '$lib/components/navbar/navbar.svelte';
	import type { PageData } from './$types';
	type Props = {
		data: PageData;
		children: () => any;
	};
	let {
		data,
		children,
	}: Props = $props();
</script>

<svelte:head>
	<title>EventSquare</title>
</svelte:head>

<div class="w-full overflow-x-hidden scroll-smooth min-h-screen hidescroll">
	<Navbar userData={data} />
	<Toaster richColors position="top-center" />
	<div class="min-h-screen">
		{@render children()}
	</div>
	<Footer />
</div>
