<script lang="ts">
	import { enhance } from '$app/forms';
	import type { SubmitFunction } from '@sveltejs/kit';

	type HiddenField = { name: string; value: string };

	let {
		title,
		description,
		action,
		hiddenFields = [],
		confirmText = 'Confirm',
		cancelText = 'Cancel',
		confirmClass = 'btn btn-primary',
		confirmDisabled = false,
		onResult
	} = $props<{
		title: string;
		description: string;
		action: string;
		hiddenFields?: HiddenField[];
		confirmText?: string;
		cancelText?: string;
		confirmClass?: string;
		confirmDisabled?: boolean;
		onResult?: SubmitFunction;
	}>();

	let dialogEl: HTMLDialogElement | null = $state(null);

	export function open() {
		dialogEl?.showModal();
	}

	export function close() {
		dialogEl?.close();
	}
</script>

<dialog bind:this={dialogEl} class="modal">
	<div class="modal-box">
		<h3 class="text-lg font-bold">{title}</h3>
		<p class="mt-2 text-base-content/70">{description}</p>

		<form
			method="POST"
			action={action}
			use:enhance={onResult}
			class="mt-6 flex justify-end gap-2"
		>
			{#each hiddenFields as f (f.name)}
				<input type="hidden" name={f.name} value={f.value} />
			{/each}
			<button type="button" class="btn" onclick={() => close()}>{cancelText}</button>
			<button type="submit" class={confirmClass} disabled={confirmDisabled}>{confirmText}</button>
		</form>
	</div>
	<form method="dialog" class="modal-backdrop"><button aria-label="Close dialog">close</button></form>
</dialog>
