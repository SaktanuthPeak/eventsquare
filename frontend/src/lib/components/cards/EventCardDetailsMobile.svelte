<script lang="ts">
	import { CalendarIcon, MapPinIcon, TagIcon, GlobeIcon, ImageIcon } from 'phosphor-svelte';
	import { cn } from '$lib/utils/tw-utils';
	import { env } from '$env/dynamic/public';
	import { fade, fly } from 'svelte/transition';

	let { eventData } = $props();

	function toValidDate(value: unknown): Date | null {
		if (value instanceof Date) {
			return Number.isNaN(value.getTime()) ? null : value;
		}
		if (typeof value === 'string' || typeof value === 'number') {
			const parsed = new Date(value);
			return Number.isNaN(parsed.getTime()) ? null : parsed;
		}
		return null;
	}

	function isSameLocalDay(a: Date, b: Date) {
		return (
			a.getFullYear() === b.getFullYear() &&
			a.getMonth() === b.getMonth() &&
			a.getDate() === b.getDate()
		);
	}

	function formatDate(startDate: unknown, endDate: unknown) {
		const start = toValidDate(startDate);
		const end = toValidDate(endDate);

		if (!start && !end) return 'Date TBA';
		if (start && !end) {
			return new Intl.DateTimeFormat('en-GB', {
				year: 'numeric',
				month: 'long',
				day: 'numeric'
			}).format(start);
		}
		if (!start && end) {
			return new Intl.DateTimeFormat('en-GB', {
				year: 'numeric',
				month: 'long',
				day: 'numeric'
			}).format(end);
		}

		// start and end are both valid here
		if (isSameLocalDay(start!, end!)) {
			return new Intl.DateTimeFormat('en-GB', {
				year: 'numeric',
				month: 'long',
				day: 'numeric'
			}).format(start!);
		}

		const startFormat = new Intl.DateTimeFormat('en-GB', {
			month: 'short',
			day: 'numeric'
		}).format(start!);

		const endFormat = new Intl.DateTimeFormat('en-GB', {
			month: 'short',
			day: 'numeric',
			year: 'numeric'
		}).format(end!);

		return `${startFormat} - ${endFormat}`;
	}

	function getEventTypeBadge(eventType: string) {
		return cn(
			'badge font-medium',
			eventType === 'public'
				? 'badge-success text-success-content'
				: 'badge-secondary text-secondary-content'
		);
	}
</script>

<div class="flex flex-col gap-4">
	<div class="w-full aspect-[2/3] overflow-hidden">
		{#if eventData?.image}
			<img
				class="w-full h-full object-cover"
				src={`${env.PUBLIC_API_URL}/v1/events/image/${eventData?.image.file_id}`}
				alt={eventData?.name}
				transition:fade={{ duration: 200 }}
			/>
		{:else}
			<div
				class="w-full h-full bg-gradient-to-br from-base-200 to-base-300 flex flex-col items-center justify-center p-4"
			>
				<ImageIcon size={48} weight="thin" class="text-base-content/30 mb-2" />
				<p class="text-base-content/50 text-center">No Image Available</p>
			</div>
		{/if}
	</div>
	<!-- Type Badge Overlay -->
	<div class="absolute top-4 right-4">
		<div class={getEventTypeBadge(eventData?.event_type)}>
			{eventData?.event_type === 'public' ? 'Public Event' : 'Private Event'}
		</div>
	</div>

	<div class="md:hidden w-full max-w-md mx-auto relative z-10" in:fly={{ y: 20, duration: 300 }}>
		<div class="card overflow-hidden bg-base-100 shadow-lg border border-base-200">
			<!-- Event Image -->

			<!-- Event Details -->
			<div class="card-body p-5">
				<h2 class="card-title text-xl font-bold">{eventData?.name}</h2>

				<div class="divider my-2"></div>

				<div class="space-y-3">
					<!-- Date -->
					<div class="flex items-center gap-2">
						<div class="bg-primary/5 p-1.5 rounded-full">
							<CalendarIcon size={18} weight="fill" class="text-primary" />
						</div>
						<span class="text-sm">
							{formatDate(eventData?.start_date, eventData?.end_date)}
						</span>
					</div>

					<!-- Location -->
					<div class="flex items-center gap-2">
						<div class="bg-primary/5 p-1.5 rounded-full">
							<MapPinIcon size={18} weight="fill" class="text-primary" />
						</div>
						<span class="text-sm line-clamp-1">{eventData?.location}</span>
					</div>

					<!-- Category -->
					<div class="flex items-center gap-2">
						<div class="bg-primary/5 p-1.5 rounded-full">
							<TagIcon size={18} weight="fill" class="text-primary" />
						</div>
						<span class="badge badge-accent text-accent-content">{eventData?.event_category}</span>
					</div>
				</div>
			</div>
		</div>
	</div>
</div>
