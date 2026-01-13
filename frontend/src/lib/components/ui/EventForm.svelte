<script lang="ts">
  import { fade, slide } from "svelte/transition";
  import TextInput from "$lib/components/ui/forms/TextInput.svelte";
  import TextArea from "$lib/components/ui/forms/TextArea.svelte";
  import DatePicker from "$lib/components/ui/forms/DatePicker.svelte";
  import FileInput from "$lib/components/ui/forms/FileInput.svelte";
  import CheckInModal from "$lib/components/modals/CheckInModal.svelte";
  import { eventCategories } from "$lib/static/event";
  import {
    Calendar,
    MapPin,
    Users,
    Clock,
    Image,
    Plus,
    Trash,
    XCircle,
    CalendarDot,
    CalendarDots,
    Info,
  } from "phosphor-svelte";
  import type { SuperForm } from "sveltekit-superforms";
  import type { createEventSchema } from "../../../routes/manager/[organization]/owner/view-events/create-event/schema";
  import type { z } from "zod";
  import SuperDebug, { fileProxy } from "sveltekit-superforms";

  let { form, mode = "create" } = $props<{
    form: SuperForm<z.infer<typeof createEventSchema>>;
    mode?: "create" | "edit";
  }>();

  const { form: formData, allErrors, enhance } = form;

  let showCheckInRangeModal = $state(false);
  let checkInRanges = $state<Array<{ start_time: string; end_time: string }>>([
    ...($formData.checkInRange || []),
  ]);

  function addCheckInRange(range: { start_time: string; end_time: string }) {
    checkInRanges = [...checkInRanges, range];
    $formData.checkInRange = checkInRanges;
  }

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
    <!-- Event Basic Info Section -->
    <div class="grid grid-cols-1 gap-6">
      <!-- Basic Info Section -->
      <div class="space-y-6 p-6 border border-primary/20 rounded-lg">
        <div class="flex gap-1 text-gray-700">
          <Info size={24} weight="fill" />
          <h3 class="text-lg font-semibold text-gray-700">Basic Information</h3>
          <span class="text-error">*</span>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <!-- Event Name -->
          <div>
            <TextInput
              {form}
              bind:value={$formData.title}
              name="title"
              label="Event Name"
              placeholder="Enter event name"
              required
            />
          </div>

          <!-- Location -->
          <div>
            <TextInput
              {form}
              bind:value={$formData.location}
              name="location"
              label="Event Location"
              placeholder="Enter event location"
              required
            />
          </div>
        </div>

        <!-- Description -->
        <div>
          <TextArea
            {form}
            bind:value={$formData.description}
            name="description"
            label="Event Description"
            placeholder="Enter event description"
            required
            rows={4}
          />
        </div>
      </div>

      <!-- Details Section -->
      <div class="space-y-6 p-6 border border-primary/20 rounded-lg">
        <div class="flex gap-1 text-gray-700">
          <Info size={24} weight="fill" />
          <h3 class="text-lg font-semibold text-gray-700">Event Details</h3>
          <span class="text-error">*</span>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <!-- Event Type -->
          <div>
            <label
              for="event_type"
              class="block text-sm font-medium text-gray-700 mb-1"
            >
              Event Type
            </label>
            <select
              id="event_type"
              bind:value={$formData.event_type}
              name="event_type"
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              required
            >
              <option value="" disabled selected hidden>Select type</option>
              <option value="public">Public</option>
              <option value="private">Private</option>
            </select>
          </div>

          <!-- Category -->
          <div>
            <label
              for="event_category"
              class="block text-sm font-medium text-gray-700 mb-1"
            >
              Event Category
            </label>
            <select
              id="event_category"
              bind:value={$formData.event_category}
              name="event_category"
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              required
            >
              <option value="" disabled selected hidden>Select category</option>
              {#each eventCategories as category}
                <option value={category}>{category}</option>
              {/each}
            </select>
          </div>

          <!-- Max Audience -->
          <div class="flex flex-col gap-0.5">
            <span>
              <label
                for="maxAudience"
                class="block text-sm font-medium text-gray-700 mb-1"
              >
                Max Audience
              </label>
            </span>
            <TextInput
              {form}
              bind:value={$formData.maxAudience}
              name="maxAudience"
              type="number"
              min="1"
              max="50"
              placeholder="Enter max audience"
              required
            />
          </div>
        </div>

        <div class="flex flex-row gap-6">
          <!-- Start Date -->
          <div class="w-[31.8%]">
            <label
              for="startDate"
              class="block text-sm font-medium text-gray-700 mb-1"
            >
              Start Date
            </label>
            <DatePicker
              {form}
              bind:value={$formData.startDate}
              name="startDate"
              placeholder="Select start date"
              required
            />
          </div>

          <!-- End Date -->
          <div class="w-[31.8%]">
            <label
              for="endDate"
              class="block text-sm font-medium text-gray-700 mb-1"
            >
              End Date
            </label>
            <DatePicker
              {form}
              bind:value={$formData.endDate}
              name="endDate"
              placeholder="Select end date"
              required
            />
          </div>
        </div>
      </div>

      <!-- Event Image -->
      <div class="p-6 border border-primary/20 rounded-lg flex flex-col gap-1">
        <div class="flex gap-1 text-gray-700">
          <h3 class="text-lg text-gray-700 font-semibold flex gap-2">
            <Image size={24} weight="fill" />
            Event Image
          </h3>
          <span class="text-error">*</span>
        </div>

        <FileInput
          {form}
          bind:files={$file}
          name="image"
          label="Upload Image"
          description="JPEG or PNG, max 5MB"
        />
      </div>

      <!-- Check-in Time Ranges Section -->
      <div class="border border-primary/20 rounded-lg p-6">
        <div class="flex justify-between items-center mb-4">
          <div>
            <h3 class="text-lg font-semibold text-gray-700 flex gap-2">
              <Clock size={24} weight="fill" />
              Check-in Time Ranges
            </h3>
            <p class="text-sm text-base-content/70">
              Define when attendees can check in to your event
            </p>
          </div>
          <button
            type="button"
            class="btn btn-primary btn-sm gap-1"
            onclick={() => (showCheckInRangeModal = true)}
          >
            <Plus size={16} weight="bold" />
            Add Range
          </button>
        </div>

        <!-- Check-in Ranges List -->
        {#if checkInRanges.length > 0}
          <div class="space-y-2 max-h-[200px] overflow-y-auto pr-2">
            {#each checkInRanges as range, index}
              <div
                class="flex justify-between items-center p-3 bg-white border border-gray-200 rounded-lg shadow-sm hover:bg-base-300 transition-colors"
                transition:slide={{ duration: 150 }}
              >
                <div class="flex items-center gap-3">
                  <Clock size={24} class="text-primary" />
                  <div>
                    <div class="font-medium">
                      {new Date(range.start_time).toLocaleString("en-US", {
                        day: "2-digit",
                        month: "short",
                        year: "numeric",
                      })}
                      {#if new Date(range.start_time).getDate() !== new Date(range.end_time).getDate()}
                        - {new Date(range.end_time).toLocaleString("en-US", {
                          day: "2-digit",
                          month: "short",
                          year: "numeric",
                        })}
                      {/if}
                    </div>
                    <div class="text-sm text-base-content/70">
                      {new Date(range.start_time).toLocaleString("en-US", {
                        hour: "2-digit",
                        minute: "2-digit",
                      })} -
                      {new Date(range.end_time).toLocaleString("en-US", {
                        hour: "2-digit",
                        minute: "2-digit",
                      })}
                    </div>
                  </div>
                </div>
                <button
                  type="button"
                  class="btn btn-sm btn-ghost text-error"
                  onclick={() => {
                    checkInRanges = checkInRanges.filter((_, i) => i !== index);
                    $formData.checkInRange = checkInRanges;
                  }}
                  aria-label="Remove range"
                >
                  <Trash size={18} />
                </button>
              </div>
            {/each}
          </div>
        {:else}
          <div
            class="p-6 bg-base-100 rounded-lg text-center flex flex-col items-center justify-center"
            transition:fade
          >
            <CalendarDots
              size={64}
              class="text-base-content/70 mb-2 "
              weight="light"
            />
            <p class="text-primary">No check-in ranges added yet.</p>
            <p class="text-sm mt-1 text-base-content/60">
              Click the "Add Range" button to define when attendees can check
              in.
            </p>
          </div>
        {/if}
      </div>

      <!-- Error Messages -->
      {#if $allErrors.length}
        <div class="bg-red-50 p-4 rounded-lg border border-red-100">
          <div class="flex">
            <div class="flex-shrink-0">
              <XCircle size={22} weight="fill" class="text-red-500" />
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
    </div>
  </form>
</div>

{#if showCheckInRangeModal}
  <CheckInModal {form} bind:showCheckInRangeModal onSave={addCheckInRange} />
{/if}
