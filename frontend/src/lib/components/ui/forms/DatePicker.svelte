<script lang="ts" module>
	import type { FormPath } from 'sveltekit-superforms';
</script>

<script lang="ts" generics="T extends Record<string, unknown>, U extends FormPath<T>">
	import FormField from './FormField.svelte';
	import type { HTMLInputAttributes } from 'svelte/elements';
	import type { BaseInputProps } from '$lib/models/baseInputProps';
	import { Label, type FieldProps } from 'formsnap';
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

	const fallbackInputId = `date-${String(name)}`;

	function onChange(event: Event) {
		const input = event.target as HTMLInputElement;
		const dateValue = input.value ? new Date(input.value) : null;
		value = dateValue ? dateValue.toISOString() : '';
	}

	let displayValue = $derived(() => {
		if (!value) return undefined;
		const date = new Date(value);
		if (Number.isNaN(date.getTime())) return undefined;
		return getLocalISOString(date);
	});
</script>

<FormField {form} {label} {name} {description}>
	{#snippet formInput({ props })}
		{@const { id: propsId, name: _propsName, ...propsWithoutIdName } = props}
		{@const { id: attrsId, ...attrsWithoutId } = attrs}
		{@const inputId = propsId ?? attrsId ?? fallbackInputId}

		<div>
			<input type="hidden" name={String(name)} value={value} />

			<div class="flex w-full flex-col gap-1">
				{#if label}
					<div class="flex gap-1">
						<Label for={inputId}>{label}</Label>
						{#if attrs.required}
							<span class="text-error">*</span>
						{/if}
					</div>
				{/if}
				<label class="block w-full cursor-pointer" for={inputId}>
					<input
						id={inputId}
						type="datetime-local"
						class={`input w-full cursor-pointer ${className}`}
						{...attrsWithoutId}
						{...propsWithoutIdName}
						name={undefined}
						value={displayValue}
						onchange={onChange}
						onclick={(e) => {
							(e.target as HTMLInputElement).showPicker?.();
						}}
					/>
				</label>
			</div>
		</div>
	{/snippet}
</FormField>