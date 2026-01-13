<script lang="ts">
	import { Camera, MagnifyingGlass } from 'phosphor-svelte';
	import type { PageData } from './$types';
	import EventCards from '$lib/components/cards/EventCards.svelte';
	import { page } from '$app/state';
	import SearchBar from '$lib/components/ui/SearchBar.svelte';
	import CategoryFilter from '$lib/components/ui/CategoryFilter.svelte';
	import EventCarousel from '$lib/components/ui/EventCarousel.svelte';
	import { cn } from '$lib/utils/tw-utils';
	import { fade } from 'svelte/transition';

	let { data, showLoginModal = $bindable() }: { data: PageData; showLoginModal: boolean } =
		$props();

	let landingPageImage = $state(false);
	const featuredEvents = $derived(data.events?.slice(0, 3) || []);
	let selectedCategory = $state('All');

	const defaultQuery = page.url.searchParams.get('search') || '';

	// Handle category change
	function handleCategoryChange(event: CustomEvent<string>) {
		selectedCategory = event.detail;
	}
</script>

<div class="flex flex-col items-center justify-center bg-base-100 w-screen">
	<!-- Hero Section -->
	<div
		class="flex justify-center w-screen items-center py-20 md:p-20 lg:grid-cols-2 bg-gradient-to-br from-[#6900FF] to-[#19003C]"
	>
		<!-- <div class="md:flex-2/7 hidden md:block">
			{#if landingPageImage}
				<img
					src={event?.image_url}
					alt={event?.title}
					class="w-full h-full object-cover rounded-t-2xl"
				/>
			{:else}
				<div class="w-full h-full flex flex-col items-center justify-center">
					<Camera size={128} class="text-base-100" weight="fill" />
					<h1 class="text-lg font-medium text-center text-base-100">No Image</h1>
				</div>
			{/if}
		</div> -->
		<div
			class=" md:flex-5/7 px-10 w-screen md:w-full text-white font-medium md:text-xl md:p-4"
			transition:fade={{ duration: 300 }}
		>
			<h1 class="text-3xl md:text-5xl font-bold mb-4">Discover Amazing Events</h1>
			<p class="text-md md:text-xl mb-6">
				Your gateway to unforgettable experiences. Find and book tickets to the hottest festivals,
				concerts, and cultural events happening around you.
			</p>
			<div class="flex justify-start gap-4">
				<a href="/events" class="btn btn-secondary">Browse Events</a>
			</div>
		</div>
	</div>

	<SearchBar {defaultQuery} customClass="max-w-[80%] md:max-w-[45%] relative bottom-[25px]" />

	<!-- Carousel -->
</div>

<section class="flex flex-col items-center justify-center w-screen bg-base-100">
	<EventCarousel {featuredEvents} />
	<!-- Category Filter Component -->
	<CategoryFilter initialCategory={selectedCategory} on:categoryChange={handleCategoryChange} />

	<!-- Events Grid Section -->
	<div class="grid grid-cols-2 md:grid-cols-3 xl:grid-cols-5 gap-4 p-2 max-w-screen w- mx-auto">
		{#if data.events && data.events
				.slice(0, 16)
				.filter((cat) => !selectedCategory || selectedCategory === 'All' || cat.event_category?.includes(selectedCategory)).length > 0}
			{#each data.events
				.slice(0, 16)
				.filter((cat) => !selectedCategory || selectedCategory === 'All' || cat.event_category?.includes(selectedCategory)) as event}
				<EventCards {event} />
			{/each}
		{:else}
			<div class="col-span-full text-center py-12">
				<p class="text-lg text-base-content/70">No events found.</p>
			</div>
		{/if}
	</div>
	<a
		href="/events"
		class="btn border-0 my-10 text-base-100 bg-gradient-to-t from-[#6900FF] to-accent hover:bg-gradient-to-t hover:from-[#5700D2] hover:to-[#6900FF] transition-colors duration-200 delay-100"
	>
		Explore More
	</a>
</section>
