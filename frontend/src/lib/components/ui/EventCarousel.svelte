<script lang="ts">
	let { featuredEvents = [] } = $props();
</script>

<div
	class="carousel rounded-2xl w-[95%] md:w-[75%] h-[500px] sm:h-96 xl:h-[500px] 2xl:h-[600px] overflow-hidden"
>
	{#each featuredEvents as event, i}
		<div id="slide{i}" class="carousel-item relative w-full h-full">
			{#if event.image_url}
				<a href={`/events/${event.id}`} class="w-full h-full block">
					<div class="w-full h-full overflow-hidden">
						<img
							src={event.image_url}
							alt={event.title}
							class="w-full h-full object-cover hover:scale-110 transition-transform duration-700"
						/>
					</div>
				</a>
			{:else}
				<a
					class="w-full h-full bg-base-200 flex items-center justify-center"
					href={`/events/${event.id}`}
				>
					<h2 class="text-2xl font-bold">{event.title}</h2>
				</a>
			{/if}

			<!-- Overlay text -->
			<a
				class="absolute bottom-0 left-0 right-0 p-4 bg-gradient-to-t from-black/80 to-transparent text-white"
				href={`/events/${event.id}`}
			>
				<h3 class="text-xl font-bold">{event.title}</h3>
				<p class="text-sm truncate">{event.description}</p>
			</a>

			<!-- Navigation buttons -->
			<div
				class="absolute flex justify-between transform -translate-y-1/2 left-5 right-5 top-1/2 z-10"
			>
				<a
					href="#slide{i === 0 ? featuredEvents.length - 1 : i - 1}"
					class="btn bg-base-100/80 backdrop-blur-sm btn-circle shadow-lg hover:bg-primary hover:text-white"
					>❮</a
				>
				<a
					href="#slide{i === featuredEvents.length - 1 ? 0 : i + 1}"
					class="btn bg-base-100/80 backdrop-blur-sm btn-circle shadow-lg hover:bg-primary hover:text-white"
					>❯</a
				>
			</div>
		</div>
	{/each}
</div>
