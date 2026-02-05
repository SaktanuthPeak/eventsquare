<script lang="ts">
  import { fade, slide } from "svelte/transition";
  import TextInput from "$lib/components/ui/forms/TextInput.svelte";
  import TextArea from "$lib/components/ui/forms/TextArea.svelte";
  import DatePicker from "$lib/components/ui/forms/DatePicker.svelte";
  import FileInput from "$lib/components/ui/forms/FileInput.svelte";
  import { eventCategories } from "$lib/static/event";
  import {
    ImageIcon,
    XCircleIcon,
    InfoIcon,
  } from "phosphor-svelte";
  import type { SuperForm } from "sveltekit-superforms";
  import SuperDebug, { fileProxy } from "sveltekit-superforms";

  let { form, mode = "create" } = $props<{
    form: SuperForm<any>;
    mode?: "create" | "edit";
  }>();

  const { form: formData, allErrors, enhance } = form;
  const file = fileProxy(form, "image");
</script>

<div
  class="mx-auto bg-white rounded-xl shadow-sm border border-base-200 overflow-hidden"
>
  <div
    class="bg-gradient-to-r from-primary/5 to-secondary/5 p-6 border-b border-base-200"
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
    enctype="multipart/form-data"
  >
    
    <!-- Details Section -->
      <div class="space-y-6 p-6 border border-primary/20 rounded-lg">
        <div class="flex gap-1 text-gray-700">
          <InfoIcon size={24} weight="fill" />
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
              bind:value={$formData.startDate}
              name="startDate"
              placeholder="Select start date"
              required
              label="Start Date"
            />
            <DatePicker
              {form}
              bind:value={$formData.endDate}
              label="End Date"
              name="endDate"
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

      <!-- Event ImageIcon -->
      <div class="p-6 border border-primary/20 rounded-lg flex flex-col gap-1">
        <div class="flex gap-1 text-gray-700">
          <h3 class="text-lg text-gray-700 font-semibold flex gap-2">
            <ImageIcon size={24} weight="fill" />
            Event Image
          </h3>
          {#if mode === 'create'}
            <span class="text-error">*</span>
          {/if}
        </div>

        <FileInput
          {form}
          bind:files={$file}
          name="image"
          label="Upload ImageIcon"
          description="JPEG or PNG, max 5MB"
        />
      </div>

      <!-- Error Messages -->
      {#if $allErrors.length}
        <div class="bg-red-50 p-4 rounded-lg border border-red-100">
          <div class="flex">
            <div class="flex-shrink-0">
              <XCircleIcon size={22} weight="fill" class="text-red-500" />
            </div>
            <div class="ml-1">
              <h3 class="text-sm font-medium text-red-800">
                Please fix the following {$allErrors.length === 1
                  ? "error"
                  : "errors"}:
              </h3>
              <div class="mt-2 text-sm text-red-700">
                <ul class="list-disc pl-5 space-y-1">
                  {#each $allErrors as error}
                    <li>
                      {#if error.path.includes("checkInRange")}
                        Check-in range: {error.messages.join(". ")}
                      {:else if error.path[0] === "_errors"}{error.messages.join(
                          ". "
                        )}
                      {:else}
                        {error.messages.join(". ")}
                      {/if}
                    </li>
                  {/each}
                </ul>
              </div>
            </div>
          </div>
        </div>
      {/if}

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
      <SuperDebug data={$formData} />
  </form>
</div>
