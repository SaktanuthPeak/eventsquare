<script lang="ts">
	import { CaretDown, User } from 'phosphor-svelte';
	import { page } from '$app/state';
	import { goto } from '$app/navigation';
	import ButtonMenuMobile from '$lib/components/btn/ButtonMenuMobile.svelte';


	let { userData } = $props();
	let scroll: boolean = $state(false);
	let menuOpen = $state(false);
	let mobileMenuOpen = $state(false);

	$effect(() => handleScroll());
	$effect(() => {
		// Close menus on navigation
		page.url.pathname;
		mobileMenuOpen = false;
		menuOpen = false;
	});

	function handleScroll() {
		if (typeof window === 'undefined') return;
		if (page.url.pathname === '/' || page.url.pathname === '/events') {
			scroll = window.pageYOffset > 10;
		} else {
			scroll = true;
		}
	}

	function closeMobileMenu() {
		mobileMenuOpen = false;
	}
</script>

<svelte:window onscroll={handleScroll} />

<header
	class={'fixed w-full navbar ' +
		(scroll ? 'shadow-2xl' : '') +
		' transition-all duration-300 z-50 flex justify-between items-center px-[16px] py-[12px] ' +
		(scroll
			? 'bg-primary text-white shadow-md h-16'
			: 'bg-transparent text-white backdrop-blur-sm  h-20')}
>
	<div class="flex gap-[4px]">
		<!--  Logo -->
		<a href="/">
			<h1
				class="w-[180px] h-fit text-3xl font-extrabold cursor-pointer focus:outline-none focus:border-transparent focus:ring-0 border-0"
			>
				EventSquare
			</h1>
		</a>
	</div>
	{#if userData.user}
		<div class="flex flex-row gap-2.5 py-[12px] justify-center place-items-center items-end">
			<!-- Mobile hamburger -->
			<div class="md:hidden">
				<ButtonMenuMobile bind:isOpen={mobileMenuOpen} />
			</div>

			<!-- Mobile avatar shortcut -->
			<button
				class="md:hidden"
				onclick={() => closeMobileMenu()}
			>
				<div
					class={'size-[40px] rounded-full overflow-hidden flex items-center justify-center ' +
						(scroll
							? 'ring-2 ring-secondary bg-neutral-content/20 '
							: 'ring-2 ring-white bg-primary-content/20 ')}
				>
					{#if userData?.user?.profile_picture || userData?.user?.avatar_url}
						<img
							src={userData?.user?.profile_picture || userData?.user?.avatar_url}
							alt="Profile"
							class="w-full h-full object-cover"
						/>
					{:else}
						<User size={24} weight="bold" class={scroll ? 'text-neutral-content' : 'text-white'} />
					{/if}
				</div>
			</button>

			<!-- Desktop user dropdown -->
			<div class="hidden md:flex flex-row gap-2.5 items-end">
				<div class="flex gap-[12px] place-items-center content-center">
					<div class="w-[220px] hidden md:block">
						<div class="text-base-100 text-sm font-semibold line-clamp-1">
							{userData.user
								? `${userData.user.first_name} ${userData.user.last_name}`
								: 'No Name'}
						</div>
						<div class="text-base-100/80 text-xs">@{userData.user.username}</div>
					</div>
				</div>
				<details class="relative" bind:open={menuOpen}>
					<summary class="list-none cursor-pointer flex flex-row items-center gap-2">
						<div
							class={'size-[40px] rounded-full overflow-hidden flex items-center justify-center ' +
								(scroll
									? 'ring-2 ring-secondary bg-neutral-content/20 '
									: 'ring-2 ring-white bg-primary-content/20 ')}
						>
							{#if userData?.user?.profile_picture || userData?.user?.avatar_url}
								<img
									src={userData?.user?.profile_picture || userData?.user?.avatar_url}
									alt="Profile"
									class="w-full h-full object-cover"
								/>
							{:else}
								<User
									size={24}
									weight="bold"
									class={scroll ? 'text-neutral-content  ' : 'text-white'}
								/>
							{/if}
						</div>
						<CaretDown
							size={12}
							weight="bold"
							class={scroll ? 'text-neutral-content  ' : 'text-white'}
						/>
					</summary>
					<ul
						class="absolute right-10 top-8 mt-2 w-40 bg-base-100 outline-1 outline-primary/20 rounded-lg shadow-lg z-50 border border-base-300 text-primary overflow-auto"
					>
						<li>
							<a
								href="/menu/profile"
								class="block px-4 py-2 hover:bg-base-200"
								onclick={() => (menuOpen = false)}>Profile</a
							>
						</li>
						<li>
							<a
								href="/menu/check-in-history"
								class="block px-4 py-2 hover:bg-base-200"
								onclick={() => (menuOpen = false)}>Check in History</a
							>
						</li>
						<li>
							<a
								href="/menu/my-tickets/active-tickets"
								class="block px-4 py-2 hover:bg-base-200"
								onclick={() => (menuOpen = false)}>My tickets</a
							>
						</li>
						{#if  userData.user.roles.includes('admin')}
							<li>
								<a
									href="/admin"
									class="block px-4 py-2 hover:bg-base-200"
									onclick={() => (menuOpen = false)}>Admin</a
								>
							</li>
						{/if}
						<li>
							<a
								href="/account/logout"
								class="block px-4 py-2 hover:bg-base-200"
								onclick={() => (menuOpen = false)}>Log Out</a
							>
						</li>
					</ul>
				</details>
			</div>
			<!-- <button
			onclick={handleLogout}
				class="ml-2 cursor-pointer hidden md:block"
				aria-label="Log out"
			>
				<SignOut size={20} class="text-neutral-content" />
			</button> -->
		</div>
	{:else}
		<div class="gap-[10px] hidden md:flex">
			<div class="flex gap-[12px]">
				<button
					class={'login-navbar-button ' + (scroll ? '' : 'bg-transparent text-white')}
					onclick={() => goto('/account/login', { replaceState: true, invalidateAll: true })}
				>
					Login
				</button>
				<button
					class={'login-navbar-button ' + (scroll ? ' ' : 'bg-transparent text-white')}
					onclick={() => goto('/account/signup', { replaceState: true, invalidateAll: true })}
				>
					Sign up
				</button>
			</div>
		</div>
		<div class="flex md:hidden">
			<ButtonMenuMobile bind:isOpen={mobileMenuOpen} />
		</div>
	{/if}
</header>

{#if mobileMenuOpen}
	<div
		class={'fixed inset-x-0 bottom-0 z-40 md:hidden ' + (scroll ? 'top-16' : 'top-20')}
		aria-label="Mobile navigation menu"
	>
		<button
			type="button"
			class="absolute inset-0 bg-black/40"
			aria-label="Close menu"
			onclick={closeMobileMenu}
		></button>
		<nav class="relative mx-4 mt-4 rounded-2xl bg-base-100 text-primary shadow-xl border border-base-200 overflow-hidden">
			<div class="p-4 border-b border-base-200">
				<div class="text-sm font-semibold">Menu</div>
				<div class="text-xs text-base-content/60 line-clamp-1">{page.url.pathname}</div>
			</div>
			<div class="p-2">
				<a href="/" class="block rounded-xl px-4 py-3 hover:bg-base-200" onclick={closeMobileMenu}
					>Home</a
				>
				<a href="/events" class="block rounded-xl px-4 py-3 hover:bg-base-200" onclick={closeMobileMenu}
					>Events</a
				>

				{#if userData.user}
					<a
						href="/menu/profile"
						class="block rounded-xl px-4 py-3 hover:bg-base-200"
						onclick={closeMobileMenu}
						>Profile</a
					>
					<a
						href="/menu/my-tickets/active-tickets"
						class="block rounded-xl px-4 py-3 hover:bg-base-200"
						onclick={closeMobileMenu}
						>My tickets</a
					>
					
					<a
						href="/menu/check-in-history"
						class="block rounded-xl px-4 py-3 hover:bg-base-200"
						onclick={closeMobileMenu}
						>Check in History</a
					>

					{#if  userData.user.roles.includes('admin')}
						<a
							href="/admin"
							class="block rounded-xl px-4 py-3 hover:bg-base-200"
							onclick={closeMobileMenu}
							>Admin</a
						>
					{/if}
					<a href="/account/logout" class="block rounded-xl px-4 py-3 hover:bg-base-200" onclick={closeMobileMenu}
						>Log Out</a
					>
				{:else}
					<div class="my-2 h-px bg-base-200"></div>
					<button
						type="button"
						class="w-full text-left rounded-xl px-4 py-3 hover:bg-base-200"
						onclick={() => {
							closeMobileMenu();
							goto('/account/login', { replaceState: true, invalidateAll: true });
						}}
					>
						Login
					</button>
					<button
						type="button"
						class="w-full text-left rounded-xl px-4 py-3 hover:bg-base-200"
						onclick={() => {
							closeMobileMenu();
							goto('/account/signup', { replaceState: true, invalidateAll: true });
						}}
					>
						Sign up
					</button>
				{/if}
			</div>
		</nav>
	</div>
{/if}

