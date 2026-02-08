<script lang="ts">
  import TextInput from "$lib/components/ui/forms/TextInput.svelte";
  import TextArea from "$lib/components/ui/forms/TextArea.svelte";
  import DatePicker from "$lib/components/ui/forms/DatePicker.svelte";
  import FileInput from "$lib/components/ui/forms/FileInput.svelte";
  import FormErrorSummary from "$lib/components/ui/forms/FormErrorSummary.svelte";
  import TicketTypeDraftEditor from "$lib/components/ui/forms/TicketTypeDraftEditor.svelte";
  import { eventCategories } from "$lib/static/event";
  import {
    Image,
    Info,
  } from "phosphor-svelte";
  import type { SuperForm } from "sveltekit-superforms";
  import SuperDebug, { fileProxy } from "sveltekit-superforms";

  let { form, mode = "create" } = $props<{
    form: SuperForm<any>;
    mode?: "create" | "edit";
  }>();

  const formData = $derived(form.form);
  const enhance = $derived(form.enhance);
  const allErrors = $derived(form.allErrors);

  const file = $derived(mode === 'edit' ? fileProxy(form, 'image') : undefined);

  // ticket_types is kept in the Superforms store via TicketTypeDraftEditor

</script>

<div
  class="mx-auto bg-white rounded-xl shadow-sm border border-base-200 overflow-hidden"
>
  <div
    class="bg-linear-to-r from-primary/5 to-secondary/5 p-6 border-b border-base-200"
  >
    <h2 class="text-2xl font-bold">
      {mode === "create" ? "Create New Event" : "Edit Event"}
    </h2>
    <p class="text-base-content/70 mt-1">
      Fill in the details to {mode === "create" ? "create your" : "update this"}
      event
    </p>
  </div>

  <form
    method="POST"
    use:enhance
    class="p-6 space-y-6"
    enctype={mode === 'edit' ? 'multipart/form-data' : undefined}
  >
    <!-- ticket_types is submitted via the superforms store (see $effect above) -->

    <!-- Details Section -->
      <div class="space-y-6 p-6 border border-primary/20 rounded-lg">
        <div class="flex gap-1 text-gray-700">
          <Info size={24} weight="fill" />
          <h3 class="text-lg font-semibold text-gray-700">Event Details</h3>
          <span class="text-error">*</span>
        </div>
        <div class="flex gap-6">
          <!-- Event Name -->
            <TextInput
              {form}
              bind:value={$formData.name}
              name="name"
              label="Event Name"
              placeholder="Enter event name"
              required
            />
    
          <!-- Location -->
            <TextInput
              {form}
              bind:value={$formData.location}
              name="location"
              label="Event Location"
              placeholder="Enter event location"
              required
            />
        </div>
    
        <!-- Description -->
          <TextArea
            {form}
            bind:value={$formData.description}
            name="description"
            label="Event Description"
            placeholder="Enter event description"
            required
            rows={4}
          />

        <div class="grid grid-cols-1  gap-6">

          <!-- Category -->
          <div>
            <label
              for="event_type"
              class="block text-sm font-medium text-gray-700 mb-1"
            >
              Event Category
            </label>
            <select
              id="event_type"
              bind:value={$formData.event_type}
              name="event_type"
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              required
            >
              <option value="" disabled selected hidden>Select category</option>
              {#each eventCategories as category}
                <option value={category}>{category}</option>
              {/each}
            </select>
          </div>
        </div>

        <div class="w-full flex gap-6">
            <DatePicker
              {form}
              bind:value={$formData.start_date}
              name="start_date"
              placeholder="Select start date"
              required
              label="Start Date"
            />
            <DatePicker
              {form}
              bind:value={$formData.end_date}
              label="End Date"
              name="end_date"
              placeholder="Select end date"
              required
            />

            <DatePicker
              {form}
              bind:value={$formData.booking_start_date}
              name="booking_start_date"
              label="Booking Start Date"
              placeholder="Select booking start date"
              required
            />
            <DatePicker
              {form}
              bind:value={$formData.booking_end_date}
              name="booking_end_date"
              label="Booking End Date"
              placeholder="Select booking end date"
              required
            />
        </div>
      </div>
        <div class="p-6 border border-base-200 rounded-lg bg-base-100">
          <h3 class="text-lg font-semibold text-gray-700">Event Image</h3>
          <p class="mt-1 text-sm text-base-content/70">
            Upload the image after creating the event (on the Ticket management page).
          </p>
        </div>
        
    {#if mode === 'create'}
      <!-- Tickets -->
      <TicketTypeDraftEditor bind:json={$formData.ticket_types} />
    {/if}

      <!-- Error Messages -->
      <FormErrorSummary errors={$allErrors} />

      <!-- Form Buttons -->
      <div class="flex justify-end gap-3 pt-4 border-t border-base-200">
        <button
          type="button"
          class="btn btn-outline"
          onclick={(e) => {
            e.preventDefault();
            history.back();
          }}
        >
          Cancel
        </button>
        <button type="submit" class="btn btn-primary min-w-32">
          {#if mode === "create"}
            Create Event
          {:else}
            Save Changes
          {/if}
        </button>
      </div>
      <!-- <SuperDebug data={{ ...$formData}} /> -->
  </form>
</div>
