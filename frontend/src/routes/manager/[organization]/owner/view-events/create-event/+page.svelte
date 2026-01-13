<script lang="ts">
  import type { PageData } from "./$types";
  import { zodClient } from "sveltekit-superforms/adapters";
  import { createEventSchema } from "./schema";
  import { toast } from "svelte-sonner";
  import { goto } from "$app/navigation";
  import { superForm } from "sveltekit-superforms";
  import EventForm from "$lib/components/ui/EventForm.svelte";

  let { data }: { data: PageData } = $props();

  const form = superForm(data.form, {
    validators: zodClient(createEventSchema),
    customValidity: true,
    onResult: async ({ result }) => {
      if (result.type === "success") {
        toast.success("Event created successfully!");
        await goto(`/manager/${data.organization_id}/owner/view-events`, {
          invalidateAll: true,
        });
      } else if (result.type === "failure") {
        toast.error(result.data?.message || "Failed to create event.");
      }
    },
    dataType: "json",
  });
</script>

<div class="mx-auto mt-[50px] px-[200px]">
  <h1 class="text-4xl font-bold mb-6">Create Event</h1>
  <EventForm {form} mode="create" />
</div>
