<script lang="ts">
  import { goto } from "$app/navigation";
  import { toast } from "svelte-sonner";
  import { superForm } from "sveltekit-superforms";
  import { zodClient } from "sveltekit-superforms/adapters";
  import { organizeSchema } from "../../../create-organizer/schema";
  import TextInput from "$lib/components/ui/forms/TextInput.svelte";
  import { Camera, ArrowLeft, User, Warning } from "phosphor-svelte";
  import type { PageData } from "./$types";
  import { bankNames } from "$lib/static/organization";

  let { data }: { data: PageData } = $props();

  // Add state to track name conflict
  let nameConflict = $state(false);
  let originalName = $state(data?.organizer?.organizer?.name || "");

  let profileImage = $state(data?.organizer?.logo_url || null);
  let fileInput: HTMLInputElement;

  function handleFileSelect(e: Event) {
    const target = e.target as HTMLInputElement;
    if (target.files && target.files[0]) {
      const reader = new FileReader();
      reader.onload = (e) => {
        profileImage = e.target?.result as string;
      };
      reader.readAsDataURL(target.files[0]);
    }
  }

  const form = superForm(data?.form, {
    dataType: "json",
    customValidity: true,
    validators: zodClient(organizeSchema),
    onResult: async ({ result }) => {
      if (result.type === "success") {
        toast.success("Organization updated successfully!");
        await goto(`/manager/${data.organization_id}/owner/dashboard`, {
          invalidateAll: true,
        });
      } else if (result.type === "failure") {
        if (
          result.status === 409 ||
          (result.data?.message &&
            result.data.message.toLowerCase().includes("already exists"))
        ) {
          nameConflict = true;
          toast.error(
            "Organization name already exists. Please choose a different name."
          );
        } else {
          toast.error(result.data?.message || "Failed to update organization.");
        }
      } else {
        toast.error("An unexpected error occurred during validation.");
        console.error("Validation failed!", result);
      }
    },
  });

  const { form: formData, allErrors, errors, submitting, enhance } = form;

  // Clear name conflict error when user changes the name
  $effect(() => {
    if (nameConflict && $formData.name !== originalName) {
      nameConflict = false;
    }
  });
</script>

<div class="max-w-4xl mx-auto px-4 py-8">
  <!-- Header with Back Button -->
  <div class="mb-8">
    <button
      class="btn btn-ghost gap-2 mb-4"
      onclick={() => goto(`/manager/${data.organization_id}/owner/dashboard`)}
    >
      <ArrowLeft size={20} />
      Back to Dashboard
    </button>
    <h1 class="text-3xl font-bold">Edit Organization</h1>
    <p class="text-base-content/70 mt-2">
      Update your organization's information and settings.
    </p>
  </div>

  <!-- Main Content -->
  <div
    class="bg-base-100 rounded-xl border border-base-300 shadow-sm overflow-hidden"
  >
    <!-- Organization Logo -->
    <div
      class="bg-gradient-to-r from-primary/10 to-secondary/10 p-8 flex justify-center"
    >
      <div class="relative">
        <div
          class="w-32 h-32 bg-base-100 rounded-full flex items-center justify-center overflow-hidden border-4 border-white shadow-md"
        >
          {#if profileImage}
            <img
              src={profileImage}
              alt="Organization logo"
              class="w-full h-full object-cover"
            />
          {:else}
            <User size={64} />
          {/if}
        </div>
        <button
          type="button"
          class="absolute bottom-0 right-0 bg-primary text-white rounded-full p-2 shadow-md hover:bg-primary-focus transition-colors"
        >
          <!-- onclick={() => fileInput?.click()} -->
          <Camera size={20} />
        </button>
        <input
          type="file"
          bind:this={fileInput}
          onchange={handleFileSelect}
          accept="image/*"
          class="hidden"
        />
      </div>
    </div>

    <!-- Form -->
    <form method="POST" class="p-6" use:enhance>
      <input type="hidden" name="organizerId" value={data.organization_id} />

      <!-- Organizer Information Section -->
      <section class="mb-8">
        <h2 class="text-xl font-semibold mb-4 pb-2 border-b">
          Organizer Information
        </h2>
        <div class="space-y-4">
          <div class="form-control">
            <label for="name" class="label">
              <span class="label-text"
                >Organizer Name <span class="text-error">*</span></span
              >
            </label>
            <TextInput
              {form}
              id="name"
              bind:value={$formData.name}
              name="name"
              placeholder="Organizer Name"
              required
            />

            {#if nameConflict}
              <div class="mt-2 flex items-start gap-2 text-error">
                <Warning size={18} weight="fill" class="flex-shrink-0 mt-0.5" />
                <p class="text-sm">
                  This organization name is already taken. Please choose a
                  different name.
                </p>
              </div>
            {/if}
          </div>
        </div>
      </section>

      <!-- Contact Information Section -->
      <section class="mb-8">
        <h2 class="text-xl font-semibold mb-4 pb-2 border-b">
          Contact Information
        </h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="form-control">
            <label for="email" class="label">
              <span class="label-text">Email</span>
            </label>
            <TextInput
              {form}
              id="email"
              bind:value={$formData.contact_information.email}
              name="contact_information.email"
              placeholder="Email"
              type="email"
            />
          </div>

          <div class="form-control">
            <label for="line_id" class="label">
              <span class="label-text">Line ID</span>
            </label>
            <TextInput
              {form}
              id="line_id"
              bind:value={$formData.contact_information.line_id}
              name="contact_information.line_id"
              placeholder="Line ID"
            />
          </div>

          <div class="form-control">
            <label for="facebook" class="label">
              <span class="label-text">Facebook</span>
            </label>
            <TextInput
              {form}
              id="facebook"
              bind:value={$formData.contact_information.facebook}
              name="contact_information.facebook"
              placeholder="Facebook"
            />
          </div>

          <div class="form-control">
            <label for="instagram" class="label">
              <span class="label-text">Instagram</span>
            </label>
            <TextInput
              {form}
              id="instagram"
              bind:value={$formData.contact_information.instagram}
              name="contact_information.instagram"
              placeholder="Instagram"
            />
          </div>

          <div class="form-control md:col-span-2">
            <label for="website_url" class="label">
              <span class="label-text">Website URL</span>
            </label>
            <TextInput
              {form}
              id="website_url"
              bind:value={$formData.contact_information.website_url}
              name="contact_information.website_url"
              placeholder="Website URL"
              type="url"
            />
          </div>
        </div>
      </section>

      <!-- Business Address Section -->
      <section class="mb-8">
        <h2 class="text-xl font-semibold mb-4 pb-2 border-b">
          Business Address
        </h2>
        <div class="space-y-4">
          <div class="form-control">
            <label for="company_name" class="label">
              <span class="label-text"
                >Company Name <span class="text-error">*</span></span
              >
            </label>
            <TextInput
              {form}
              id="company_name"
              bind:value={$formData.business_address.company_name}
              name="business_address.company_name"
              placeholder="Company Name"
              required
            />
          </div>

          <div class="form-control">
            <label for="company_address" class="label">
              <span class="label-text"
                >Company Address <span class="text-error">*</span></span
              >
            </label>
            <TextInput
              {form}
              id="company_address"
              bind:value={$formData.business_address.company_address}
              name="business_address.company_address"
              placeholder="Company Address"
              required
            />
          </div>

          <div class="form-control">
            <label for="company_phone" class="label">
              <span class="label-text"
                >Company Phone <span class="text-error">*</span></span
              >
            </label>
            <TextInput
              {form}
              id="company_phone"
              bind:value={$formData.business_address.company_phone}
              name="business_address.company_phone"
              placeholder="Company Phone"
              required
            />
          </div>
        </div>
      </section>

      <!-- Banking Information Section -->
      <section class="mb-8">
        <h2 class="text-xl font-semibold mb-4 pb-2 border-b">
          Banking Information
        </h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="form-control">
            <label for="bank_name" class="label">
              <span class="label-text"
                >Bank Name <span class="text-error">*</span></span
              >
            </label>
            <select
              id="bank_name"
              bind:value={$formData.banking_information.bank_name}
              name="banking_information.bank_name"
              class="select select-bordered w-full"
              required
            >
              <option value="" disabled selected>Select a bank</option>
              {#each bankNames as bankName}
                <option value={bankName}>{bankName}</option>
              {/each}
            </select>
          </div>

          <div class="form-control">
            <label for="account_number" class="label">
              <span class="label-text"
                >Account Number <span class="text-error">*</span></span
              >
            </label>
            <TextInput
              {form}
              id="account_number"
              bind:value={$formData.banking_information.account_number}
              name="banking_information.account_number"
              placeholder="10-15 digits"
              required
            />
          </div>

          <div class="form-control md:col-span-2">
            <label for="account_name" class="label">
              <span class="label-text"
                >Account Name <span class="text-error">*</span></span
              >
            </label>
            <TextInput
              {form}
              id="account_name"
              bind:value={$formData.banking_information.account_name}
              name="banking_information.account_name"
              placeholder="Name on bank account"
              required
            />
          </div>
        </div>
      </section>

      <!-- Error Display -->
      {#if $allErrors.length}
        <div class="bg-error/10 p-4 rounded-lg mb-6 border border-error/20">
          <h4 class="font-semibold text-error mb-2">
            Please fix the following errors:
          </h4>
          <ul class="list-disc ml-6 text-sm">
            {#each $allErrors as error}
              <li class="text-error">{error.messages.join(". ")}</li>
            {/each}
          </ul>
        </div>
      {/if}

      <!-- Action Buttons -->
      <div class="flex flex-col sm:flex-row gap-3 mt-8">
        <button
          class="btn btn-outline"
          onclick={() =>
            goto(`/manager/${data.organization_id}/owner/view-events`)}
        >
          Cancel
        </button>
        <button type="submit" class="btn btn-primary" disabled={$submitting}>
          {$submitting ? "Saving..." : "Save Changes"}
        </button>
      </div>
    </form>
  </div>
  <!-- <SuperDebug data={$formData} /> -->
</div>

<style>
</style>
