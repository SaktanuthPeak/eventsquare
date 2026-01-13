<script lang="ts">
	import type { PageData } from './$types';
	import EventCards from '$lib/components/cards/EventCards.svelte';
	import SearchBar from '$lib/components/ui/SearchBar.svelte';
	import { page } from '$app/state';
	import CategoryFilter from '$lib/components/ui/CategoryFilter.svelte';
	import EventCarousel from '$lib/components/ui/EventCarousel.svelte';

	let { data }: { data: PageData } = $props();
	const defaultQuery = page.url.searchParams.get('search') || '';
	let selectedCategory = $state('All');

	function handleCategoryChange(event: CustomEvent<string>) {
		selectedCategory = event.detail;
	}
</script>

<div
	class="flex flex-col items-center justify-center w-full bg-base-100 overflow-visible mb-[20px]"
>
	<div class="bg-gradient-to-tr to-accent from-pink-500 h-[300px] p-16 w-screen">
		<div class="flex flex-row gap-4 justify-center items-center"></div>
	</div>
	<SearchBar {defaultQuery} customClass="max-w-[70%] md:max-w-[45%]  relative bottom-[25px]" />
	<CategoryFilter initialCategory={selectedCategory} on:categoryChange={handleCategoryChange} />
	<div class="grid grid-cols-2 md:grid-cols-3 xl:grid-cols-5 gap-6 p-6 max-w-screen-xl mx-auto">
		{#if data.events && data.events.filter((cat) => !selectedCategory || selectedCategory === 'All' || cat.event_category?.includes(selectedCategory)).length > 0}
			{#each data.events.filter((cat) => !selectedCategory || selectedCategory === 'All' || cat.event_category?.includes(selectedCategory)) as event}
				<EventCards {event} />
			{/each}
		{:else}
			<div class="col-span-full text-center py-12">
				<p class="text-lg text-base-content/70">No events found.</p>
			</div>
		{/if}
	</div>
</div>
