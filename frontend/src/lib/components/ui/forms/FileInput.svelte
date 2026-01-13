<script lang="ts" module>
  import type { FormPath } from "sveltekit-superforms";
</script>

<!-- svelte-ignore non_reactive_update -->
<script
  lang="ts"
  generics="T extends Record<string, unknown>, U extends FormPath<T>"
>
  import { Label, type FieldProps } from "formsnap";
  import FormField from "./FormField.svelte";
  import type { BaseInputProps } from "$lib/models/baseInputProps";

  import type { HTMLInputAttributes } from "svelte/elements";
  import { env } from "$env/dynamic/public";

  type InputProps = Omit<HTMLInputAttributes, "form"> &
    BaseInputProps &
    FieldProps<T, U>;

  let {
    form,
    label,
    name,
    description,
    files = $bindable(),
    ...attrs
  }: InputProps = $props();

  const { form: formData } = form;
  let previewUrl = $state<string | null>(null);
  let previousFile = $state<File | null>(null);

  $effect(() => {
    if (files?.length && files[0] instanceof File) {
      const currentFile = files[0];
      if (currentFile !== previousFile) {
        if (previewUrl && previewUrl.startsWith("blob:"))
          URL.revokeObjectURL(previewUrl);
        previewUrl = URL.createObjectURL(currentFile);
        previousFile = currentFile;
      }
      return;
    }

    if ($formData.image?.file_id) {
      previewUrl = `${env.PUBLIC_API_URL}/v1/events/image/${$formData.image.file_id}`;
      previousFile = null;
      return;
    }

    if (previewUrl && previewUrl.startsWith("blob:")) {
      URL.revokeObjectURL(previewUrl);
    }
    previewUrl = null;
    previousFile = null;
  });
</script>

<FormField {form} {label} {name} {description}>
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
  {/snippet}
</FormField>

{#if previewUrl}
  <div class="mt-2">
    <img
      src={previewUrl}
      alt="Preview"
      class="w-64 h-auto"
      onload={() => console.log("Image loaded")}
      onerror={(e) => console.error("Image load error:", e)}
    />
  </div>
{/if}
