<script lang="ts">
	import { env } from '$env/dynamic/public';

	let { featuredEvents = [] } = $props<{ featuredEvents?: any[] }>();

	const apiBase = env.PUBLIC_BASE_API_URL || env.PUBLIC_API_URL || 'http://localhost:9000';

	function eventTitle(event: any): string {
		return String(event?.title ?? event?.name ?? 'Event');
	}

	function eventDescription(event: any): string {
		return String(event?.description ?? '');
	}

	function eventImageUrl(event: any): string | null {
		if (event?.image_url) return String(event.image_url);
		if (event?.image_id) return `${apiBase}/v1/images/${event.image_id}`;
		return null;
	}
</script>

<div
	class="carousel rounded-2xl w-[95%] md:w-[75%] h-125 sm:h-96 xl:h-125 2xl:h-150 overflow-hidden"
>
	{#each featuredEvents as event, i}
		<div id="slide{i}" class="carousel-item relative w-full h-full">
			{#if eventImageUrl(event)}
				<a href={`/events/${event.id}`} class="w-full h-full block">
					<div class="w-full h-full overflow-hidden">
						<img
							src={eventImageUrl(event) ?? ''}
							alt={eventTitle(event)}
							class="w-full h-full object-cover hover:scale-110 transition-transform duration-700"
						/>
					</div>
				</a>
			{:else}
				<a
					class="w-full h-full bg-base-200 flex items-center justify-center"
					href={`/events/${event.id}`}
				>
					<h2 class="text-2xl font-bold">{eventTitle(event)}</h2>
				</a>
			{/if}

			<!-- Overlay text -->
			<a
				class="absolute bottom-0 left-0 right-0 p-4 bg-linear-to-t from-black/80 to-transparent text-white"
				href={`/events/${event.id}`}
			>
				<h3 class="text-xl font-bold">{eventTitle(event)}</h3>
				<p class="text-sm truncate">{eventDescription(event)}</p>
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
