<script lang="ts">
	import { User } from 'phosphor-svelte';

	let { userData, isMenuOpen = $bindable(), isOpen = $bindable() } = $props();

	function toggleMenu() {
		isOpen = false;
		isMenuOpen = false;
	}
</script>

<container
	class={' hidden md:flex md:flex-col items-center justify-center w-full h-full bg-white ring-1 ring-primary/20 rounded-2xl overflow-auto px-0'}
>
	{#if userData.user}
		<div
			class="flex flex-col gap-2.5 w-full pt-[30px] pb-[20px] shadow-lg bg-primary justify-center place-items-center content-center items-center"
		>
			<div
				class={'size-[40px] rounded-full overflow-hidden flex items-center justify-center ring-2 ring-white bg-white/20 '}
			>
				{#if userData?.user?.profile_picture || userData?.user?.avatar_url}
					<img
						src={userData?.user?.profile_picture || userData?.user?.avatar_url}
						alt="Profile"
						class="w-full h-full object-cover"
					/>
				{:else}
					<User size={24} weight="bold" class={'text-white  '} />
				{/if}
			</div>
			<div class="flex gap-[12px] place-items-center content-center">
				<div class="w-full md:flex md:flex-col md:gap-1 hidden">
					<div class="text-white text-sm font-semibold line-clamp-1">
						{userData.user ? `${userData.user.first_name} ${userData.user.last_name}` : 'No Name'}
					</div>
					<div class="text-white/60 text-xs">
						@{userData.user.username}
					</div>
				</div>
			</div>
		</div>
	{:else}
		<h1 class="text-2xl font-bold text-primary">Please log in to view your profile</h1>
	{/if}
	<ul class="menu flex flex-col items-start justify-start w-full p-2 gap-2">
		<a
			href="/menu/profile"
			onclick={() => {
				toggleMenu();
			}}
			class="p-2 w-full hover:bg-primary/10 rounded-xl cursor-pointer select-none"
		>
			<li>Profile</li>
		</a>
		<a
			href="/menu/check-in-history"
			class="p-2 w-full hover:bg-primary/10 rounded-xl cursor-pointer select-none"
		>
			<li>Check-in History</li>
		</a>
		<a
			href="/menu/my-tickets/active-tickets"
			onclick={() => {
				toggleMenu();
			}}
			class="p-2 w-full hover:bg-primary/10 rounded-xl cursor-pointer select-none"
		>
			<li>My Tickets</li>
		</a>
		<a
			href="/menu/purchase-history"
			onclick={() => {
				toggleMenu();
			}}
			class="p-2 w-full hover:bg-primary/10 rounded-xl cursor-pointer select-none"
		>
			<li>Purchase history</li>
		</a>
	</ul>
</container>
