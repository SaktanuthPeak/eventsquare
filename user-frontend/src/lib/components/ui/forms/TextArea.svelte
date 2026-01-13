<script lang="ts" module>
  import type { FormPath } from "sveltekit-superforms";
</script>

<script
  lang="ts"
  generics="T extends Record<string, unknown>, U extends FormPath<T>"
>
  import { Label, type FieldProps } from "formsnap";
  import FormField from "./FormField.svelte";
  import type { BaseInputProps } from "$lib/models/baseInputProps";

  type InputProps = Omit<HTMLTextAreaElement, "form"> &
    BaseInputProps &
    FieldProps<T, U>;

  let {
    form,
    label,
    name,
    description,
    value = $bindable(),
  }: InputProps = $props();
</script>

<FormField {form} {label} {name} {description}>
  {#snippet formInput({ props })}
    <div class="flex w-full flex-col gap-1">
      <Label>{label}</Label>
      <textarea class="textarea w-full" {...props} bind:value></textarea>
    </div>
  {/snippet}
</FormField>
