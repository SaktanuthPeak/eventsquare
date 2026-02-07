<script lang="ts">
  import { fade, slide } from "svelte/transition";
  import TextInput from "$lib/components/ui/forms/TextInput.svelte";
  import TextArea from "$lib/components/ui/forms/TextArea.svelte";
  import DatePicker from "$lib/components/ui/forms/DatePicker.svelte";
  import FileInput from "$lib/components/ui/forms/FileInput.svelte";
  import { eventCategories } from "$lib/static/event";
  import {
    Image,
    XCircle,
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

  const file = $derived(fileProxy(form, "image"));

  type TicketDraft = {
    name: string;
    total: number;
    price: number;
  };

  let ticketDrafts = $state<TicketDraft[]>([
    { name: '', total: 1, price: 0 }
  ]);

  function addTicketDraft() {
    ticketDrafts = [...ticketDrafts, { name: '', total: 1, price: 0 }];
  }

  function removeTicketDraft(index: number) {
    ticketDrafts = ticketDrafts.filter((_, i) => i !== index);
    if (ticketDrafts.length === 0) ticketDrafts = [{ name: '', total: 1, price: 0 }];
  }

  function ticketTypesJsonValue(): string {
    return JSON.stringify(normalizedTicketTypes());
  }

  function normalizedTicketTypes(): Array<{ name: string; total: number; price: number; remaining: number }> {
    return ticketDrafts
      .map((t) => ({
        name: String(t.name ?? '').trim(),
        total: Number(t.total ?? 0),
        price: Number(t.price ?? 0),
        remaining: Number(t.total ?? 0)
      }))
      .filter((t) => t.name.length > 0);
  }

  // Store-only submission to avoid duplicate keys when using use:enhance
  $effect(() => {
    const json = ticketTypesJsonValue();
    if ($formData.ticket_types !== json) {
      $formData.ticket_types = json;
    }
  });

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
    enctype="multipart/form-data"
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

      <!-- Event Image -->
      <div class="p-6 border border-primary/20 rounded-lg flex flex-col gap-1">
        <div class="flex gap-1 text-gray-700">
          <h3 class="text-lg text-gray-700 font-semibold flex gap-2">
            <Image size={24} weight="fill" />
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
          label="Upload Image"
          description="JPEG or PNG, max 5MB"
        />
      </div>

    {#if mode === 'create'}
      <!-- Tickets -->
      <div class="space-y-4 p-6 border border-primary/20 rounded-lg">
        <div class="flex items-center justify-between gap-3">
          <h3 class="text-lg font-semibold text-gray-700">Ticket Types</h3>
          <button type="button" class="btn btn-sm btn-outline" onclick={addTicketDraft}>
            Add ticket
          </button>
        </div>

        <div class="space-y-3">
          {#each ticketDrafts as t, i (i)}
            <div class="grid grid-cols-1 gap-3 md:grid-cols-12 items-end">
              <div class="md:col-span-6">
                <label class="block text-sm font-medium text-gray-700 mb-1" for={`ticket-name-${i}`}>Name</label>
                <input
                  id={`ticket-name-${i}`}
                  class="input input-bordered w-full"
                  placeholder="e.g. VIP"
                  value={t.name}
                  oninput={(e) => {
                    const value = (e.target as HTMLInputElement).value;
                    ticketDrafts = ticketDrafts.map((x, idx) => (idx === i ? { ...x, name: value } : x));
                  }}
                />
              </div>
              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-gray-700 mb-1" for={`ticket-total-${i}`}>Total</label>
                <input
                  id={`ticket-total-${i}`}
                  class="input input-bordered w-full"
                  type="number"
                  min="1"
                  value={t.total}
                  oninput={(e) => {
                    const value = Number((e.target as HTMLInputElement).value);
                    ticketDrafts = ticketDrafts.map((x, idx) =>
                      idx === i ? { ...x, total: Number.isFinite(value) ? value : 0 } : x
                    );
                  }}
                />
              </div>
              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-gray-700 mb-1" for={`ticket-price-${i}`}>Price</label>
                <input
                  id={`ticket-price-${i}`}
                  class="input input-bordered w-full"
                  type="number"
                  min="0"
                  value={t.price}
                  oninput={(e) => {
                    const value = Number((e.target as HTMLInputElement).value);
                    ticketDrafts = ticketDrafts.map((x, idx) =>
                      idx === i ? { ...x, price: Number.isFinite(value) ? value : 0 } : x
                    );
                  }}
                />
              </div>
              <div class="md:col-span-2 flex justify-end">
                <button
                  type="button"
                  class="btn btn-sm btn-ghost text-error"
                  onclick={() => removeTicketDraft(i)}
                >
                  Remove
                </button>
              </div>
            </div>
          {/each}
        </div>
        <p class="text-sm text-base-content/60">
          You can add more than 1 ticket type. Remaining will start equal to Total.
        </p>
      </div>
    {/if}

      <!-- Error Messages -->
      {#if $allErrors.length}
        <div class="bg-red-50 p-4 rounded-lg border border-red-100">
          <div class="flex">
            <div class="shrink-0">
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
      <!-- <SuperDebug data={{ ...$formData, ticket_types: normalizedTicketTypes() }} /> -->
  </form>
</div>
