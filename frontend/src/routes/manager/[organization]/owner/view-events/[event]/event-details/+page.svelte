<script lang="ts">
  import type { PageData } from "./$types";
  import { fileProxy, superForm } from "sveltekit-superforms/client";
  import { zodClient } from "sveltekit-superforms/adapters";
  import { createEventSchema } from "../../create-event/schema";
  import { toast } from "svelte-sonner";
  import { goto } from "$app/navigation";
  import EventForm from "$lib/components/ui/EventForm.svelte";

  let { data }: { data: PageData } = $props();

  const form = superForm(data.form, {
    validators: zodClient(createEventSchema),
    customValidity: true,
    onResult: async ({ result }) => {
      if (result.type === "success") {
        toast.success("Edit event successfully!");
        await goto(`/manager/${data.organization_id}/owner/view-events`, {
          invalidateAll: true,
        });
      } else if (result.type === "failure") {
        toast.error(result.data?.error || "Failed to edit event.");
      }
    },
    dataType: "json",
  });

  const { form: formData } = form;

  $formData.startDate = data.start_date ? data.start_date.toISOString() : "";
  $formData.endDate = data.end_date ? data.end_date.toISOString() : "";
</script>

<div class="mx-auto">
  <EventForm {form} mode="edit" />
</div>
