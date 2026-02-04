<script lang="ts" module>
	import type { FormPath } from 'sveltekit-superforms';
</script>

<script lang="ts" generics="T extends Record<string, unknown>, U extends FormPath<T>">
	import {
		Field,
		type FieldProps,
		FieldErrors,
		Control,
		Label,
		type ControlAttrs,
		Description
	} from 'formsnap';
	import type { ComponentProps, Snippet } from 'svelte';
	import type { BaseInputProps } from '$lib/models/baseInputProps';

	type Props = {
		formInput: Snippet<[{ props: Expand<ControlAttrs> }]>;
		hideErrors?: boolean; // Add this prop
	} & BaseInputProps &
		FieldProps<T, U> &
		ComponentProps<typeof Control>;

	let {
		form,
		name,
		description,
		children: childrenProps,
		formInput,
		hideErrors = false, // Default to showing errors
		...restProps
	}: Props = $props();
</script>

<Field {form} {name}>
	<Control {...restProps}>
		{#snippet children({ props })}
			{@render formInput({ props })}
		{/snippet}
	</Control>
	{#if description}
		<Description>{description}</Description>
	{/if}

	<!-- Only show errors if hideErrors is false -->
	{#if !hideErrors}
		<FieldErrors>
			{#snippet children({ errors, errorProps })}
				<span class="text-error" {...errorProps}>
					{errors.toString().replace(',', ', ')}
				</span>
			{/snippet}
		</FieldErrors>
	{/if}
</Field>
