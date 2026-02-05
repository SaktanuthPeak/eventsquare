<script lang="ts" module>
	import type { FormPath } from 'sveltekit-superforms';
</script>

<script lang="ts" generics="T extends Record<string, unknown>, U extends FormPath<T>">
	import { Label, type FieldProps } from 'formsnap';
	import FormField from './FormField.svelte';
	import type { BaseInputProps } from '$lib/types/baseInputProps';
	import type { HTMLTextareaAttributes } from 'svelte/elements';

	type TextareaProps = Omit<HTMLTextareaAttributes, 'form'> &
		BaseInputProps &
		FieldProps<T, U> & {
			class?: string;
			value?: string;
		};

	let {
		form,
		label,
		name,
		description,
		value = $bindable(''),
		class: className = '',
		...attrs
	}: TextareaProps = $props();
</script>

<FormField {form} {label} {name} {description}>
	{#snippet formInput({ props })}
		<div class="flex h-fit w-full flex-col gap-1">
			{#if label}
				<Label class="text-lg text-black">{label}</Label>
			{/if}
			<textarea class="textarea w-full {className}" {...attrs} {...props} bind:value></textarea>
		</div>
	{/snippet}
</FormField>