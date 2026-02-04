<script lang="ts">
	import { CaretDown } from 'phosphor-svelte';
	import { User } from 'phosphor-svelte';
	import { page } from '$app/state';
	import { goto } from '$app/navigation';


	let { userData } = $props();
	let scroll: boolean = $state(false);
	let menuOpen = $state(false);

	$effect(() => handleScroll());

	function handleScroll() {
		if (page.url.pathname === '/' || page.url.pathname === '/events') {
			scroll = window.pageYOffset > 10;
		} else {
			scroll = true;
		}
	}
</script>

<svelte:window on:scroll={handleScroll} />

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
			<div class="flex gap-[12px] place-items-center content-center">
				<div class="w-[220px] hidden md:block">
					<div class="text-base-100 text-sm font-semibold line-clamp-1">
						{userData.user ? `${userData.user.first_name} ${userData.user.last_name}` : 'No Name'}
					</div>
					<div class="text-base-100/80 text-xs">
						@{userData.user.username}
					</div>
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
					<li>
						<a
							href="/menu/purchase-history"
							class="block px-4 py-2 hover:bg-base-200"
							onclick={() => (menuOpen = false)}>Order</a
						>
					</li>
					<li>
						<a
							href="/logout"
							class="block px-4 py-2 hover:bg-base-200"
							onclick={() => (menuOpen = false)}>Log Out</a
						>
					</li>
				</ul>
			</details>
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
			<button class="mr-4" onclick={() => goto('/account/login', { replaceState: true, invalidateAll: true })} aria-label="Login"
				>Login
			</button>
			|
			<button class="ml-4" onclick={() => goto('/account/signup', { replaceState: true, invalidateAll: true })} aria-label="Sign up"
				>Sign up</button
			>
		</div>
	{/if}
</header>

