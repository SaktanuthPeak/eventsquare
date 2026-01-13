<script lang="ts">
  import { X, Camera } from "phosphor-svelte"; // Add Camera icon
  import { goto } from "$app/navigation";
  import { toast } from "svelte-sonner";
  import SuperDebug, { superForm } from "sveltekit-superforms";
  import { organizeSchema } from "./schema";
  import { zodClient } from "sveltekit-superforms/adapters";
  import TextInput from "$lib/components/ui/forms/TextInput.svelte";
  import type { PageData } from "./$types";
  import { bankNames } from "$lib/static/organization";

  type Props = {
    data?: PageData;
    showCreateOrgModal?: boolean;
  };
  let { data, showCreateOrgModal = $bindable() }: Props = $props();

  const form = superForm(
    data?.form ?? {
      name: "",
      manager_id: "",
      co_manager_id: [],
      staffs_id: [],
      maximum_event: 3,
      contact_information: {
        email: "",
        line_id: "",
        facebook: "",
        instagram: "",
        website_url: "",
      },
      business_address: {
        company_name: "",
        company_address: "",
        company_phone: "",
      },
      banking_information: {
        bank_name: null as unknown as
          | "ธนาคารกรุงไทย"
          | "ธนาคารกรุงเทพ"
          | "ธนาคารกสิกรไทย"
          | "ธนาคารไทยพาณิชย์"
          | "ธนาคารกรุงศรีอยุธยา",
        account_number: "",
        account_name: "",
      },
    },
    {
      dataType: "json",
      customValidity: true,
      validators: zodClient(organizeSchema),
      onResult: async ({ result }) => {
        if (result.type === "success") {
          toast.success("Organization created successfully!");
          showCreateOrgModal = false;
          await goto(`/manager/${data?.organization_id}/owner/view-events`, {
            invalidateAll: true,
          });
        } else if (result.type === "failure") {
          toast.error(result.data?.message || "Failed to create organization.");
        } else {
          toast.error("An unexpected error occurred during validation.");
          console.error("Validation failed!", result);
        }
      },
    }
  );

  const {
    form: formData,
    allErrors,
    errors,
    constraints,
    submitting,
    enhance,
  } = form;
</script>

{#if showCreateOrgModal}
  <div
    onclose={() => (showCreateOrgModal = false)}
    class="modal modal-open min-w-screen max-w-screen sm:modal-middle"
  >
    <div class="modal-box create-org-modal hidescroll">
      <!-- Header -->
      <div class="flex justify-between items-center">
        <h3 class="font-bold text-lg text-start">Create Organizer</h3>
        <button
          type="button"
          class="btn btn-sm btn-circle btn-ghost"
          onclick={() => (showCreateOrgModal = false)}
          aria-label="Close"
        >
          <X size={18} />
        </button>
      </div>
      <!-- Avatar -->
      <div class="flex justify-center">
        <div class="relative">
          <div
            class="w-20 h-20 bg-neutral-100 rounded-full flex items-center justify-center"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-10 w-10 text-neutral-400"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
              <circle cx="12" cy="7" r="4"></circle>
            </svg>
          </div>
          <div
            class="absolute bottom-0 right-0 bg-white rounded-full p-1 shadow-md"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-4 w-4"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <path
                d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"
              ></path>
              <circle cx="12" cy="13" r="4"></circle>
            </svg>
          </div>
        </div>
      </div>

      <form
        method="POST"
        class="w-full"
        action="/manager/create-organizer"
        use:enhance
      >
        <!-- Organizer Information Section -->
        <section class="create-org-form-section">
          <h4 class="create-org-form-section-title">Organizer Information</h4>
          <div class="create-org-form-section-container">
            {$errors.name}
            <div
              class="form-control flex flex-col sm:flex-row w-full justify-center items-center"
            >
              <label for="name" class="create-org-label text-center">
                Organizer Name <span class="text-error">*</span>
              </label>
              <TextInput
                {form}
                id="name"
                bind:value={$formData.name}
                name="name"
                placeholder="Organizer Name"
                class="create-org-input"
                hideErrors={true}
                required
              />
            </div>
          </div>
        </section>

        <section class="create-org-form-section">
          <h4 class="create-org-form-section-title">Contact Information</h4>
          <div class="create-org-form-section-container">
            <div
              class="form-control flex flex-col sm:flex-row w-full justify-center items-center"
            >
              <label for="email" class="create-org-label text-center">
                Email
              </label>
              <TextInput
                {form}
                id="email"
                bind:value={$formData.contact_information.email}
                name="contact_information.email"
                placeholder="Email"
                class="create-org-input"
                hideErrors={true}
              />
            </div>
            <div class="form-control create-org-form-section-content">
              <label for="line_id" class="create-org-label text-center">
                Line ID
              </label>
              <TextInput
                {form}
                id="line_id"
                bind:value={$formData.contact_information.line_id}
                name="contact_information.line_id"
                placeholder="Line ID"
                class="create-org-input"
                hideErrors={true}
              />
            </div>
            <div class="form-control create-org-form-section-content">
              <label for="facebook" class="create-org-label text-center">
                Facebook
              </label>
              <TextInput
                {form}
                id="facebook"
                bind:value={$formData.contact_information.facebook}
                name="contact_information.facebook"
                placeholder="Facebook"
                class="create-org-input"
                hideErrors={true}
              />
            </div>
            <div class="form-control create-org-form-section-content">
              <label for="instagram" class="create-org-label text-center">
                Instagram
              </label>
              <TextInput
                {form}
                id="instagram"
                bind:value={$formData.contact_information.instagram}
                name="contact_information.instagram"
                placeholder="Instagram"
                class="create-org-input"
                hideErrors={true}
              />
            </div>
            <div class="form-control create-org-form-section-content">
              <label for="website_url" class="create-org-label text-center">
                Website URL
              </label>
              <TextInput
                {form}
                id="website_url"
                bind:value={$formData.contact_information.website_url}
                name="contact_information.website_url"
                placeholder="Website URL"
                class="create-org-input"
                hideErrors={true}
              />
            </div>
          </div>
        </section>

        <!-- Business Address Section - Now matching format -->
        <section class="create-org-form-section">
          <h4 class="create-org-form-section-title">Business Address</h4>
          <div class="create-org-form-section-container">
            <div
              class="form-control flex flex-col sm:flex-row w-full justify-center items-center"
            >
              <label for="company_name" class="create-org-label text-center">
                Company Name <span class="text-error">*</span>
              </label>
              <TextInput
                {form}
                id="company_name"
                bind:value={$formData.business_address.company_name}
                name="business_address.company_name"
                placeholder="Company Name"
                class="create-org-input"
                hideErrors={true}
                required
              />
            </div>
            <div class="form-control create-org-form-section-content">
              <label for="company_address" class="create-org-label text-center">
                Company Address <span class="text-error">*</span>
              </label>
              <TextInput
                {form}
                id="company_address"
                bind:value={$formData.business_address.company_address}
                name="business_address.company_address"
                placeholder="Company Address"
                class="create-org-input"
                hideErrors={true}
                required
              />
            </div>

            <!-- {$errors.business_address.company_phone} -->
            <div class="form-control create-org-form-section-content">
              <label for="company_phone" class="create-org-label text-center">
                Company Phone <span class="text-error">*</span>
              </label>
              <TextInput
                {form}
                id="company_phone"
                bind:value={$formData.business_address.company_phone}
                name="business_address.company_phone"
                placeholder="Company Phone"
                class="create-org-input"
                hideErrors={true}
                required
              />
            </div>
          </div>
        </section>
        <section class="create-org-form-section">
          <h4 class="create-org-form-section-title">Banking Information</h4>
          <div class="create-org-form-section-container">
            <!-- Bank Name (Dropdown) -->
            <div class="form-control create-org-form-section-content">
              <label for="bank_name" class="create-org-label text-center">
                Bank Name <span class="text-error">*</span>
              </label>
              <select
                id="bank_name"
                bind:value={$formData.banking_information.bank_name}
                name="banking_information.bank_name"
                class="create-org-input"
                required
              >
                <option value="" disabled selected>Select a bank</option>
                {#each bankNames as bankName}
                  <option value={bankName}>{bankName}</option>
                {/each}
              </select>
            </div>

            <!-- Account Number -->
            <div class="form-control create-org-form-section-content">
              <label for="account_number" class="create-org-label text-center">
                Account Number <span class="text-error">*</span>
              </label>
              <TextInput
                {form}
                id="account_number"
                bind:value={$formData.banking_information.account_number}
                name="banking_information.account_number"
                placeholder="10-15 digits"
                class="create-org-input"
                hideErrors={true}
                required
              />
            </div>

            <!-- Account Name -->
            <div class="form-control create-org-form-section-content">
              <label for="account_name" class="create-org-label text-center">
                Account Name <span class="text-error">*</span>
              </label>
              <TextInput
                {form}
                id="account_name"
                bind:value={$formData.banking_information.account_name}
                name="banking_information.account_name"
                placeholder="Name on bank account"
                class="create-org-input"
                hideErrors={true}
                required
              />
            </div>
          </div>
        </section>

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

        <!-- Buttons -->
        <div class="form-control flex justify-center gap-2 mt-6">
          <button
            onclick={() => (showCreateOrgModal = false)}
            class="btn btn-outline rounded-full"
          >
            Cancel
          </button>
          <button
            type="submit"
            class="btn btn-primary"
            disabled={$submitting || $allErrors.length > 0}
          >
            {$submitting ? "Creating..." : "Create"}
          </button>
        </div>
      </form>
    </div>
  </div>
{/if}

<style>
</style>
