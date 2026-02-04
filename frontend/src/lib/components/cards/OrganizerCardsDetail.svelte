<script lang="ts">
	import { MapTrifold, PhoneCall, User } from 'phosphor-svelte';

	let { organizer } = $props();
</script>

<div class="flex flex-col gap-2 mt-4 w-full rounded-2xl p-4 shadow-lg">
	<div class="flex flex-col gap-2">
		<h3 class="font-bold text-xl md:text-2xl">Organizer</h3>
		<hr class="border-primary" />
		<div class=" flex flex-row gap-2 items-center h-full">
			<div class="flex flex-row h-full items-center justify-center">
				{#if organizer?.images}
					<img
						class="size-[80px] object-cover rounded-full"
						src={organizer?.images[0].url}
						alt={organizer?.name}
					/>
				{:else}
					<div
						class="size-[80px] flex overflow-hidden items-center justify-center rounded-full bg-accent"
					>
						<User size={48} class="text-white" />
					</div>
				{/if}
			</div>

			<div class=" flex flex-col p-4 w-full gap-2 items-start justify-items-start h-full">
				<span class="text-2xl font-semibold pb-0 line-clamp-2 truncate">
					{organizer?.name}
				</span>
				<span class="text-sm flex flex-row gap-2 font-medium pb-0">
					<div class="h-[20px] w-[20px] justify-center">
						<MapTrifold size={20} weight="bold" />
					</div>
					<p class="text-sm font-normal pb-0 line-clamp-2 flex flex-row gap-2">
						{organizer?.business_address?.company_address}
					</p>
				</span>

				<span class="text-sm flex flex-row gap-2 font-medium pb-0">
					<div class="h-[20px] w-[20px] justify-center">
						<PhoneCall size={20} weight="bold" />
					</div>
					<p class="text-sm font-light pb-0 flex flex-row gap-2">
						{organizer?.business_address?.company_phone}
					</p>
				</span>
			</div>
		</div>
	</div>
</div>
