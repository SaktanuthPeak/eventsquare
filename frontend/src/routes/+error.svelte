<script lang="ts">
	import { page } from '$app/state';
	import { onMount } from 'svelte';
</script>

<div class="flex flex-col text-center h-screen">
	<div class="mx-auto my-auto flex flex-col gap-5">
		<p class="text-4xl">{page.status} {page.error?.message}</p>
		<div>
			<button onclick={() => history.go(-1)} class="btn btn-primary text-white"> Go Back </button>
		</div>
	</div>
</div>
