<script lang="ts">
	import type { Snippet } from 'svelte';
	import type { LayoutData } from './$types';
	import SideNavbar from '$lib/components/navbar/menuNavbar.svelte';
	import { goto } from '$app/navigation';
	import { CaretLeft, SignOutIcon } from 'phosphor-svelte';
	import MenuButton from '$lib/components/btn/ButtonMenuMobile.svelte';
	import { fade } from 'svelte/transition';

	let isMenuOpen = $state(false);
	let { data, children }: { data: LayoutData; children: Snippet } = $props();
	$effect(() => {
		if (!data.user) {
			goto('/');
		}
	});
</script>

<main
	class="md:flex justify-self-center w-[90%] xl:w-[70%] mt-[70px] bg-base-100 min-h-screen max-w-screen"
>
	<container
		class={'flex flex-col md:flex-row w-full items-start justify-items-center justify-center gap-1 md:gap-8 lg:p-8 '}
	>
		<nav
			class="flex-2/7 flex flex-row md:flex-col place-items-center md:items-start justify-start gap-3.5 w-full"
		>
			<a
				href="/"
				class="rounded-2xl transition-colors text-primary hover:underline-offset-1 hover:underline w-full"
			>
				<div class="flex items-center gap-1">
					<CaretLeft size={14} weight="bold" />
					<span class="font-bold mr-1"> Back </span>
				</div>
			</a>

			<SideNavbar userData={data} />
			<a
				href="/account/logout"
				class="w-full btn btn-outline text-primary/80 md:flex flex-row gap-1 hidden"
			>
				Log out <SignOutIcon size={16} weight="bold" />
			</a>
			<MenuButton bind:isOpen={isMenuOpen} />
		</nav>
		{#if isMenuOpen}
			<div class="md:hidden bg-base-100 w-screen mb-4">
				<nav class="flex flex-col gap-4">
					<a href="/menu/profile" class="py-2 border-b" transition:fade={{ duration: 150 }}
						>Profile</a
					>
					<a href="/menu/check-in-history" class="py-2 border-b" transition:fade={{ duration: 250 }}
						>Check-in History</a
					>
					<a
						href="/menu/my-tickets/active-tickets"
						class="py-2 border-b"
						transition:fade={{ duration: 350 }}>My tickets</a
					>
					<a href="/menu/purchase-history" class="py-2 border-b" transition:fade={{ duration: 450 }}
						>Purchase history</a
					>
				</nav>
			</div>
		{/if}
		<content
			class="flex-5/7 w-full md:w-screen flex items-center justify-center rounded-2xl p-6 bg-white outline-1 outline-primary/20"
		>
			{@render children()}
		</content>
	</container>
</main>
