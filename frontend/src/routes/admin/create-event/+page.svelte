<script lang="ts">
  import type { PageData } from './$types';
  import { zodClient } from 'sveltekit-superforms/adapters';
  import { eventFormSchema } from '$lib/schemas/eventSchema';
  import { toast } from 'svelte-sonner';
  import { goto } from '$app/navigation';
  import { superForm } from 'sveltekit-superforms';
  import { get } from 'svelte/store';
  import EventForm from '$lib/components/ui/EventForm.svelte';
  import type { z } from 'zod';

  let { data } = $props<{ data: PageData }>();

  const form = $derived.by(() =>
    superForm<z.infer<typeof eventFormSchema>>(data.form as any, {
      validators: zodClient(eventFormSchema as any),
      customValidity: true,
      onSubmit: async () => {
        console.log('[DEBUG] Submitting create event form with data:', get(form.form));
      },
      onResult: async ({ result }) => {
        console.log(result);
        if (result.type === 'success') {
          toast.success('Event created successfully!');
          const createdEventId = (result.data as any)?.createdEventId as string | undefined;
          if (createdEventId) {
            await goto(`/admin/events/${createdEventId}/tickets`, { invalidateAll: true });
          } else {
            await goto('/admin', { invalidateAll: true });
          }
        } else if (result.type === 'failure') {
          toast.error(result.data?.message || 'Failed to create event.');
        }
      },
      dataType: 'json'
    })
  );
</script>

<div class="mx-auto py-16 px-50">
  <h1 class="text-4xl font-bold mb-6">Create Event</h1>
  <EventForm {form} mode="create" />
</div>