<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import {
		CaretLeft,
		CaretRight,
		Camera,
		GameController,
		Headphones,
		User,
		UsersThree,
		Heart,
		MapPin,
		Ticket,
		FilmSlate,
		Desk,
		Confetti,
		Image,
		MicrophoneStage,
		DotsThreeOutline
	} from 'phosphor-svelte';

	// Props
	let { initialCategory = 'All', customCategories = undefined } = $props();

	// Event dispatcher
	const dispatch = createEventDispatcher<{
		categoryChange: string;
	}>();

	// State variables
	let selectedCategory = $state(initialCategory);
	let categories = $state(
		customCategories || [
			{ title: 'All', icon: 'DotsThreeOutline' },
			{ title: 'Concert', icon: 'MicrophoneStage' },
			{ title: 'Festival', icon: 'Confetti' },
			{ title: 'Theater', icon: 'FilmSlate' },
			{ title: 'Exhibition', icon: 'Image' },
			{ title: 'Workshop', icon: 'Desk' },
			{ title: 'Game', icon: 'GameController' },
			{ title: 'Music', icon: 'Headphones' },
			{ title: 'Art', icon: 'Camera' },
			{ title: 'Sports', icon: 'UsersThree' },
			{ title: 'Education', icon: 'User' },
			{ title: 'Health', icon: 'Heart' }
		]
	);

	// DOM element reference
	let categoryContainer: HTMLDivElement;

	// Handle category selection
	function handleCategoryClick(category: string) {
		selectedCategory = selectedCategory === category ? 'All' : category;
		dispatch('categoryChange', selectedCategory);
	}

	// Scroll functions
	function scrollLeft() {
		if (categoryContainer) {
			categoryContainer.scrollBy({
				left: -300,
				behavior: 'smooth'
			});
		}
	}

	function scrollRight() {
		if (categoryContainer) {
			categoryContainer.scrollBy({
				left: 300,
				behavior: 'smooth'
			});
		}
	}
</script>

<div class="flex flex-row gap-3 justify-center items-center w-[95%] md:w-[70%]">
	<button
		class="size-[32px] rounded-full shadow-lg bg-base-100 flex items-center justify-center cursor-pointer"
		onclick={scrollLeft}
	>
		<CaretLeft size={20} weight="bold" class="text-accent" />
	</button>
	<div
		class="snap-x max-w-[75%] hidescroll overflow-x-auto snap-mandatory flex flex-row items-center justify-start gap-3 bg-base-100 my-[15px]"
		bind:this={categoryContainer}
	>
		{#each categories as cat}
			<button
				class="snap-start rounded-full w-fit p-1.5 flex flex-row items-center justify-center gap-2 transition-colors duration-200 delay-100 cursor-pointer
  {selectedCategory === cat.title
					? 'bg-gradient-to-l from-[#5700D2] to-[#6900FF] text-white'
					: 'bg-accent/25 hover:bg-gradient-to-l hover:from-[#5700D2] hover:to-[#6900FF] hover:text-white'}"
				onclick={() => handleCategoryClick(cat.title)}
			>
				<div
					class="rounded-full shadow-md size-[24px] bg-base-300 flex items-center justify-center {selectedCategory ===
					cat.title
						? 'text-white'
						: 'text-accent'}"
				>
					{#if cat.icon === 'DotsThreeOutline'}
						<DotsThreeOutline size={16} weight="bold" class="text-accent" />
					{:else if cat.icon === 'User'}
						<User size={16} weight="bold" class="text-accent" />
					{:else if cat.icon === 'MapPin'}
						<MapPin size={16} weight="bold" class="text-accent" />
					{:else if cat.icon === 'Ticket'}
						<Ticket size={16} weight="bold" class="text-accent" />
					{:else if cat.icon === 'FilmSlate'}
						<FilmSlate size={16} weight="bold" class="text-accent" />
					{:else if cat.icon === 'Desk'}
						<Desk size={16} weight="bold" class="text-accent" />
					{:else if cat.icon === 'Confetti'}
						<Confetti size={16} weight="bold" class="text-accent" />
					{:else if cat.icon === 'Image'}
						<Image size={16} weight="bold" class="text-accent" />
					{:else if cat.icon === 'MicrophoneStage'}
						<MicrophoneStage size={16} weight="bold" class="text-accent" />
					{:else if cat.icon === 'UsersThree'}
						<UsersThree size={16} weight="bold" class="text-accent" />
					{:else if cat.icon === 'GameController'}
						<GameController size={16} weight="bold" class="text-accent" />
					{:else if cat.icon === 'Headphones'}
						<Headphones size={16} weight="bold" class="text-accent" />
					{:else if cat.icon === 'Camera'}
						<Camera size={16} weight="bold" class="text-accent" />
					{:else if cat.icon === 'Heart'}
						<Heart size={16} weight="bold" class="text-accent" />
					{/if}
				</div>
				<div class="select-none font-medium mr-2">
					<p class="text-lg font-medium">{cat.title}</p>
				</div>
			</button>
		{/each}
	</div>
	<button
		class="size-[32px] rounded-full shadow-lg bg-base-100 flex items-center justify-center cursor-pointer"
		onclick={scrollRight}
	>
		<CaretRight size={20} weight="bold" class="text-accent" />
	</button>
</div>
