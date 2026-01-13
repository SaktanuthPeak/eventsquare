<script lang="ts" module>
	import type { FormPath } from 'sveltekit-superforms';
</script>

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

		value = $bindable(''),
		hideErrors = false, // Default to showing errors
		...attrs
	}: InputProps = $props();
</script>

<FormField {form} {label} {name} {description} {hideErrors}>
	{#snippet formInput({ props })}
		<div class="flex w-full flex-col">
			<Label>{label}</Label>
			<input type="text" class="input w-full" {...attrs} {...props} bind:value />
		</div>
	{/snippet}
</FormField>
