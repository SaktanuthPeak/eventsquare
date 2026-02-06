<script lang="ts">
	import { Calendar, MapPin, Tag, Globe, Users, Clock } from 'phosphor-svelte';
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

	function isSameUtcDay(a: Date, b: Date) {
		return (
			a.getUTCFullYear() === b.getUTCFullYear() &&
			a.getUTCMonth() === b.getUTCMonth() &&
			a.getUTCDate() === b.getUTCDate()
		);
	}

	function formatDateRange(startDate: unknown, endDate: unknown) {
		const start = toValidDate(startDate);
		const end = toValidDate(endDate);

		if (!start && !end) return 'Date TBA';
		if (start && !end) {
			return new Intl.DateTimeFormat('en-GB', {
				year: 'numeric',
				month: 'long',
				day: 'numeric',
				timeZone: 'UTC'
			}).format(start);
		}
		if (!start && end) {
			return new Intl.DateTimeFormat('en-GB', {
				year: 'numeric',
				month: 'long',
				day: 'numeric',
				timeZone: 'UTC'
			}).format(end);
		}

		if (isSameUtcDay(start!, end!)) {
			return new Intl.DateTimeFormat('en-GB', {
				year: 'numeric',
				month: 'long',
				day: 'numeric',
				timeZone: 'UTC'
			}).format(start!);
		}

		const startFormat = new Intl.DateTimeFormat('en-GB', {
			month: 'short',
			day: 'numeric',
			timeZone: 'UTC'
		}).format(start!);

		const endFormat = new Intl.DateTimeFormat('en-GB', {
			month: 'short',
			day: 'numeric',
			year: 'numeric',
			timeZone: 'UTC'
		}).format(end!);

		return `${startFormat} - ${endFormat}`;
	}

	function getEventTypeBadge(eventType: string) {
		return cn('badge font-medium', eventType === 'public' ? 'badge-success' : 'badge-secondary');
	}
</script>

<div class="md:flex md:flex-col items-center justify-center hidden z-10">
	<div
		class="overflow-hidden bg-base-100 shadow-lg border border-base-200 rounded-xl w-full max-w-2xl"
		in:fly={{ y: 20, duration: 400 }}
	>
		<div class="flex flex-col">
			<!-- Event Image Section -->
			<div class="w-full aspect-[4/3] overflow-hidden">
				{#if eventData?.image_id}
					<img
						class="w-full h-full object-cover hover:scale-105 transition-all duration-500"
						src={`${env.PUBLIC_API_URL}/v1/images/${eventData?.image_id}`}
						alt={eventData?.name}
					/>
				{:else}
					<div
						class="w-full h-full bg-gradient-to-br from-primary/5 to-secondary/5 flex flex-col items-center justify-center p-4"
					>
						<svg
							xmlns="http://www.w3.org/2000/svg"
							class="h-16 w-16 text-primary/20 mb-3"
							fill="none"
							viewBox="0 0 24 24"
							stroke="currentColor"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="1.5"
								d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
							/>
						</svg>
						<p class="text-sm text-base-content/60">No Event Image</p>
					</div>
				{/if}
			</div>

			<!-- Event Details Section -->
			<div class="p-6">
				<!-- Header with Title and Type -->
				<div class="mb-4">
					<div class="flex flex-wrap justify-between items-start gap-3 mb-2">
						<h2 class="text-2xl font-bold leading-tight">{eventData?.name || 'Event Title'}</h2>
					</div>
					<div class="badge badge-accent text-xs font-medium">
						{eventData?.event_type || 'Uncategorized'}
					</div>
				</div>

				<!-- Details Grid -->
				<div class="flex flex-col gap-4 mt-5">
					<!-- Date -->
					<div class="flex items-center gap-3">
						<div class="bg-primary/10 p-2 rounded-full">
							<Calendar size={20} weight="fill" class="text-primary" />
						</div>
						<div class="flex flex-col">
							<span class="text-xs text-base-content/70">Date</span>
							<span class="text-sm font-medium">
								{formatDateRange(eventData?.start_date, eventData?.end_date)}
							</span>
						</div>
					</div>

					<!-- Location -->
					<div class="flex items-center gap-3">
						<div class="bg-primary/10 p-2 rounded-full">
							<MapPin size={20} weight="fill" class="text-primary" />
						</div>
						<div class="flex flex-col">
							<span class="text-xs text-base-content/70">Location</span>
							<span class="text-sm font-medium truncate">
								{eventData?.location || 'Location not specified'}
							</span>
						</div>
					</div>

					<!-- Capacity (if available) -->
					{#if eventData?.maxAudience}
						<div class="flex items-center gap-3">
							<div class="bg-primary/10 p-2 rounded-full">
								<Users size={20} weight="fill" class="text-primary" />
							</div>
							<div class="flex flex-col">
								<span class="text-xs text-base-content/70">Capacity</span>
								<span class="text-sm font-medium">{eventData.maxAudience} attendees</span>
							</div>
						</div>
					{/if}

					<!-- Time (if available) -->
					{#if eventData?.start_time}
						<div class="flex items-center gap-3">
							<div class="bg-primary/10 p-2 rounded-full">
								<Clock size={20} weight="fill" class="text-primary" />
							</div>
							<div class="flex flex-col">
								<span class="text-xs text-base-content/70">Time</span>
								<span class="text-sm font-medium">
									{new Date(eventData.start_time).toLocaleTimeString([], {
										hour: '2-digit',
										minute: '2-digit'
									})}
								</span>
							</div>
						</div>
					{/if}
				</div>
			</div>
		</div>
	</div>
</div>
