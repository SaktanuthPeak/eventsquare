<script lang="ts">
  import SuperDebug, { superForm, fileProxy } from "sveltekit-superforms";
  import type { PageData } from "./$types";
  import { toast } from "svelte-sonner";
  import { goto } from "$app/navigation";
  import FileInput from "$lib/components/ui/forms/FileInput.svelte";
  import { zodClient } from "sveltekit-superforms/adapters";
  import { uploadImgSchema } from "./schema";

  let { data }: { data: PageData } = $props();
  const form = superForm(data.form, {
    validators: zodClient(uploadImgSchema),
    onResult: ({ result }) => {
      if (result.type === "success") {
        toast.success("Image uploaded successfully!");
        goto("/manager");
      } else if (result.type === "error") {
        toast.error(result.error);
      }
    },
    dataType: "form",
  });

  const { form: formData, enhance } = form;
  const file = fileProxy(form, "image");
</script>

<div class="container mx-auto px-4 pt-4">
  <h1 class="text-4xl font-bold mb-6">Upload Image</h1>

  <div class="px-4 form-control">
    <form
      method="POST"
      enctype="multipart/form-data"
      use:enhance
      class="space-y-4"
    >
      <FileInput
        {form}
        bind:files={$file}
        name="image"
        label="Upload Image"
        description="Select an image to upload"
        required
      />
      <div class="flex justify-end">
        <button type="submit" class="btn btn-primary"> Upload </button>
      </div>
      <!-- <SuperDebug data={$formData} /> -->
    </form>
  </div>
</div>
