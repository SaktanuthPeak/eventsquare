<script lang="ts">
  import type { PageData } from "./$types";
  import { zodClient } from "sveltekit-superforms/adapters";
  import { eventSchema } from "$lib/schemas/eventSchema";
  import { toast } from "svelte-sonner";
  import { goto } from "$app/navigation";
  import { superForm } from "sveltekit-superforms";
  import EventForm from "$lib/components/ui/EventForm.svelte";
  import type { z } from "zod";

  let { data }: { data: PageData } = $props();

  const form = superForm<z.infer<typeof eventSchema>>(data.form as any, {
    validators: zodClient(eventSchema as any),
    customValidity: true,
    onResult: async ({ result }) => {
      if (result.type === "success") {
        toast.success("Event created successfully!");
        await goto(`/admin`, {
          invalidateAll: true,
        });
      } else if (result.type === "failure") {
        toast.error(result.data?.message || "Failed to create event.");
      }
    },
    dataType: "form",
  });
</script>

<div class="mx-auto py-16 px-[200px]">
  <h1 class="text-4xl font-bold mb-6">Create Event</h1>
  <EventForm {form} mode="create" />
</div>