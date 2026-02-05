<script lang="ts" module>
	import type { FormPath } from 'sveltekit-superforms';
</script>

<script lang="ts" generics="T extends Record<string, unknown>, U extends FormPath<T>">
	import FormField from './FormField.svelte';
	import type { HTMLInputAttributes } from 'svelte/elements';
	import type { BaseInputProps } from '$lib/models/baseInputProps';
	import { Label, type FieldProps } from 'formsnap';
	import { onMount } from 'svelte';
	import { getLocalISOString } from '$lib/utils/date-utils';

	type DatePickerProps = Omit<HTMLInputAttributes, 'form'> & BaseInputProps & FieldProps<T, U> & {};

	let {
		form,
		name,
		label,
		description,
		class: className = '',
		value = $bindable(''),
		...attrs
	}: DatePickerProps = $props();

	function onChange(event: Event) {
		const input = event.target as HTMLInputElement;
		const dateValue = input.value ? new Date(input.value) : null;
		value = dateValue ? dateValue.toISOString() : '';
	}

	let defaultValue = $state<string | undefined>(undefined);
	onMount(() => {
		if (value) {
			const date = new Date(value);
			defaultValue = getLocalISOString(date);
		} else {
			defaultValue = undefined;
		}
	});
</script>

<FormField {form} {label} {name} {description}>
	{#snippet formInput({ props })}
		<div>
			<div class="flex w-full flex-col gap-1">
				<div class="flex gap-1">
					<Label>{label}</Label>
					{#if attrs.required}
						<span class="text-error">*</span>
					{/if}
				</div>
				<input
					type="datetime-local"
					class={`input w-full ${className}`}
					{...attrs}
					{...props}
					value={defaultValue}
					onchange={onChange}
					onclick={(e) => {
						(e.target as HTMLInputElement).showPicker?.();
					}}
				/>
			</div>
		</div>
	{/snippet}
</FormField>