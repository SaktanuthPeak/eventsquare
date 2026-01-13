<script lang="ts">
  import { toast } from "svelte-sonner";
  import type { PageData } from "./$types";
  import { goto } from "$app/navigation";
  import SuperDebug, { superForm } from "sveltekit-superforms";
  import { zodClient } from "sveltekit-superforms/adapters";
  import { createETicketSchema } from "./schema";
  import TextInput from "$lib/components/ui/forms/TextInput.svelte";
  import { Plus, X } from "phosphor-svelte";
  import MutiDatePicker from "$lib/components/ui/forms/MutiDatePicker.svelte";

  type Props = {
    data?: PageData;
    showCreateETicketModal?: boolean;
    organizationId?: string;
    eventId?: string;
  };

  let {
    data,
    showCreateETicketModal = $bindable(),
    organizationId = $bindable(""),
    eventId = $bindable(""),
  }: Props = $props();

  const form = superForm(
    data?.form ?? {
      event_id: eventId,
      name: "",
      description: "",
      ticket_status: "avaliable",
      price: 0,
      audienceQuantity: 0,
      maxPerUser: 0,
      allowedDates: [],
    },
    {
      validators: zodClient(createETicketSchema),
      customValidity: true,

      onResult: ({ result }) => {
        if (result.type === "success") {
          toast.success("Ticket type created successfully");
          showCreateETicketModal = false;
        } else if (result.type === "error") {
          toast.error(result.error);
        }
      },
      dataType: "json",
    }
  );

  const { form: formData, allErrors, enhance } = form;
</script>

{#if showCreateETicketModal}
  <div class="modal modal-open">
    <div
      class="modal-box overflow-visible z-[50] create-ticket-modal bg-base-100 text-primary p-6"
    >
      <div class="flex justify-between items-center">
        <h3 class="font-bold text-3xl">Create E-Ticket</h3>
        <button
          class="btn btn-sm btn-circle btn-ghost"
          onclick={() => (showCreateETicketModal = false)}
        >
          <X size={18} />
        </button>
      </div>
      <div>
        <form
          method="POST"
          action="/manager/{organizationId}/owner/view-events/{eventId}/tickets-type/create-tickets-type"
          use:enhance
          class="space-y-6"
        >
          <div class="flex flex-2col gap-4">
            <!-- Ticket Name -->
            <TextInput
              {form}
              bind:value={$formData.name}
              name="name"
              label="Name"
              placeholder="Enter the name of the e-ticket"
              hideErrors={true}
              required
            />
            <!-- Ticket Description -->
            <TextInput
              {form}
              bind:value={$formData.description}
              name="description"
              label="Description"
              placeholder="Enter a description for the e-ticket"
              hideErrors={true}
              required
            />
          </div>

          <div class="flex flex-row gap-4">
            <!-- Ticket Status -->
            <div class="form-control w-full">
              <label for="ticketStatus" class="label pb-1.5">
                <span class="label-text text-black">Ticket Status</span>
              </label>
              <select
                bind:value={$formData.ticket_status}
                name="ticketStatus"
                class="select select-bordered w-full"
                placeholder="Select the status of the e-ticket"
                required
              >
                <option value="" disabled selected>Select ticket status</option>
                <option value="avaliable">Available</option>
                <option value="disable">Disable</option>
              </select>
            </div>

            <!-- Ticket Allow Per User -->
            <div class="form-control w-full">
              <label for="maxPerUser" class="label pb-1.5">
                <span class="label-text text-black">Ticket Allow Per User</span>
              </label>
              <TextInput
                {form}
                bind:value={$formData.maxPerUser}
                name="maxPerUser"
                type="number"
                placeholder="Enter the max tickets allowed per user"
                hideErrors={true}
                min="0"
                required
              />
            </div>
            <!-- Ticket Price -->
            <div class="form-control w-full">
              <label for="price" class="label pb-1.5">
                <span class="label-text text-black">Price</span>
              </label>
              <TextInput
                {form}
                bind:value={$formData.price}
                name="price"
                type="number"
                placeholder="Enter the price of the e-ticket"
                hideErrors={true}
                min="0"
                required
              />
            </div>

            <!-- Audience Quantity -->
            <div class="form-control w-full">
              <label for="audienceQuantity" class="label pb-1.5">
                <span class="label-text text-black">Audience Quantity</span>
              </label>
              <TextInput
                {form}
                bind:value={$formData.audienceQuantity}
                name="audienceQuantity"
                type="number"
                placeholder="Enter the audience quantity for the e-ticket"
                hideErrors={true}
                min="0"
                required
              />
            </div>

            <!-- allow date -->
          </div>
          <div>
            <label for="allowedDates" class="label text-black pb-1.5">
              Allowed Dates
            </label>
            <MutiDatePicker
              name="allowedDates"
              required={true}
              bind:values={$formData.allowedDates}
              placeholder="Select allowed dates for the e-ticket"
            />
          </div>

          {#if $allErrors.length}
            <div class="bg-error/10 p-3 rounded-lg mb-4 border border-error/20">
              <h4 class="font-semibold text-error">
                Please fix the following errors:
              </h4>
              <ul class="list-disc ml-4 mt-2 text-sm text-start">
                {#each $allErrors as error}
                  <li class="text-error">{error.messages.join(". ")}</li>
                {/each}
              </ul>
            </div>
          {/if}
          <div class="my-[10px] flex justify-end">
            <button type="submit" class="btn btn-primary"> Create </button>
          </div>
        </form>
      </div>

      <!-- <SuperDebug data={$formData} /> -->
    </div>
    <button
      type="button"
      class="modal-backdrop"
      aria-label="Close modal"
      onclick={() => (showCreateETicketModal = false)}
    ></button>
  </div>
{/if}
