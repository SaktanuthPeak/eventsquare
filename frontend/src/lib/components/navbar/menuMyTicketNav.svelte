<script lang="ts">
	import { cn } from '$lib/utils/tw-utils';
</script>

<div class="flex flex-col gap-[10px] w-full">
	<div class="w-full flex flex-col border-b-[1.7px] border-base-content/25">
		<div class="w-full flex flex-row justify-between items-center">
			<div class="w-full flex flex-row items-center">
				<!-- Overview -->
				<a class={cn('event-navbar-event-ctrl-btn')} href="/menu/my-tickets/active-tickets"
					><p class="line-clamp-1">Active Tickets</p></a
				>

				<!-- Event Details -->
				<a class="event-navbar-event-ctrl-btn" href="/menu/my-tickets/ended-tickets">
					<p class="line-clamp-1">Ended tickets</p></a
				>
			</div>
		</div>
	</div>
</div>
