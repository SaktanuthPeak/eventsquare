<script lang="ts">
	import Flatpickr from 'svelte-flatpickr';
	import 'flatpickr/dist/flatpickr.css';

	export let date: string;
	export let name: string | undefined = undefined;
	export let disableTime: boolean = false;
	export let dateFormat: string = 'Z';
</script>

<Flatpickr class="input input-bordered w-full" options={{ enableTime: !disableTime, altInput: true, altFormat: 'd-m-Y H:i', dateFormat: dateFormat, defaultDate: date ? new Date(date) : new Date().setHours(7, 0, 0, 0) }} bind:formattedValue={date} />

<!-- section for raws input -->
{#if name}
	<input class="hidden" {name} bind:value={date} />
{/if}