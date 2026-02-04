<script lang="ts" module>
	import type { FormPath } from 'sveltekit-superforms';
</script>

<!-- svelte-ignore non_reactive_update -->
<script lang="ts" generics="T extends Record<string, unknown>, U extends FormPath<T>">
	import { Label, type FieldProps } from 'formsnap';
	import FormField from './FormField.svelte';
	import type { BaseInputProps } from '$lib/models/baseInputProps';

	import type { HTMLInputAttributes } from 'svelte/elements';

	type InputProps = Omit<HTMLInputAttributes, 'form'> &
		BaseInputProps &
		FieldProps<T, U> & {
			hideErrors?: boolean; // Add this prop
		};

	let {
		form,
		label,
		name,
		description,
		hideErrors = false,
		files = $bindable(),
		...attrs
	}: InputProps = $props();

	let previewUrl: string | null = null;

	$effect(() => {
		if (files && files.length > 0 && files[0] instanceof File) {
			if (previewUrl) URL.revokeObjectURL(previewUrl);
			previewUrl = URL.createObjectURL(files[0]);
		}
	});
</script>

<FormField {form} {label} {name} {description} {hideErrors}>
	{#snippet formInput({ props })}
		<div class="flex w-full flex-col gap-1">
			<Label>{label}</Label>
			<input
				type="file"
				class="file-input w-full"
				accept="image/*"
				{...attrs}
				{...props}
				bind:files
			/>
		</div>
		<!-- Todo Now preview doesnt show up -->
		{#if previewUrl}
			<div class="mt-2">
				<img src={previewUrl} alt="Preview" class="mt-2 max-h-48 w-auto rounded shadow border" />
			</div>
		{/if}
	{/snippet}
</FormField>
