<script lang="ts">
  import { X } from "phosphor-svelte";
  import { goto } from "$app/navigation";
  import { toast } from "svelte-sonner";
  import SuperDebug, { superForm } from "sveltekit-superforms";
  import { signupSchema } from "./schema";
  import { zodClient } from "sveltekit-superforms/adapters";
  import TextInput from "$lib/components/ui/forms/TextInput.svelte";
  import type { PageData } from "../$types";

  type Props = {
    data?: PageData;
    showSignupModal?: boolean;
  };
  let { data, showSignupModal = $bindable() }: Props = $props();

  const form = superForm(
    data?.form ?? {
      email: "",
      username: "",
      password: "",
      confirm_password: "",
      status: "active",
      first_name: "",
      last_name: "",
    },
    {
      validators: zodClient(signupSchema),
      customValidity: true,
      onResult: async ({ result }) => {
        if (result.type === "success") {
          toast.success("Account created successfully!");
          showSignupModal = false;
          await goto("/");
        } else {
          if (result.status === 409) {
            toast.error(result.data?.error ?? "Username already exists.");
          } else {
            toast.error("An error occurred during signup.");
          }
        }
      },
    }
  );

  const {
    form: formData,
    errors,
    allErrors,
    constraints,
    submitting,
    enhance,
  } = form;
</script>

{#if showSignupModal}
  <div
    onclose={() => (showSignupModal = false)}
    class="modal modal-open min-w-screen max-w-screen sm:modal-middle"
  >
    <div class="modal-box bg-base-100 text-primary p-6 hidescroll">
      <div class="mb-3">
        <div class="flex justify-between items-center">
          <h3 class="font-bold text-lg">Sign Up to EventSquare</h3>
          <button
            type="button"
            class="btn btn-sm btn-circle btn-ghost"
            onclick={() => (showSignupModal = false)}
            aria-label="Close"
          >
            <X size={18} />
          </button>
        </div>
        <dd>Welcome our future organizer</dd>
      </div>

      <form
        method="POST"
        action="/register"
        class="flex flex-col gap-4"
        use:enhance
      >
        <div class="flex flex-row gap-3">
          <div class="form-control w-full">
            <TextInput
              {form}
              bind:value={$formData.first_name}
              name="first_name"
              label="First name"
              placeholder="Enter your first name"
              class="input input-bordered w-full"
            />
          </div>
          <div class="form-control w-full">
            <TextInput
              {form}
              bind:value={$formData.last_name}
              name="last_name"
              label="Last name"
              placeholder="Enter your last name"
              class="input input-bordered w-full"
            />
          </div>
        </div>

        <div class="form-control">
          <TextInput
            {form}
            bind:value={$formData.email}
            name="email"
            label="Email"
            placeholder="Enter your Email"
            class="input input-bordered w-full {$errors.email
              ? 'input-error'
              : ''}"
            {...$constraints.email}
          />
        </div>

        <div class="form-control">
          <TextInput
            {form}
            bind:value={$formData.username}
            name="username"
            label="Username"
            placeholder="Enter your username"
            class="input input-bordered w-full {$errors.username
              ? 'input-error'
              : ''}"
            {...$constraints.username}
          />
        </div>

        <div class="form-control">
          <TextInput
            {form}
            bind:value={$formData.password}
            name="password"
            type="password"
            label="Password"
            placeholder="Enter your password"
            class="input input-bordered w-full {$errors.password
              ? 'input-error'
              : ''}"
            {...$constraints.password}
          />
        </div>

        <div class="form-control">
          <TextInput
            {form}
            bind:value={$formData.confirm_password}
            name="confirm_password"
            type="password"
            label="Confirm Password"
            placeholder="Confirm your password"
            class="input input-bordered w-full {$errors.confirm_password
              ? 'input-error'
              : ''}"
            {...$constraints.confirm_password}
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

        <div class="form-control mt-2">
          <button
            type="submit"
            class="btn btn-primary w-full"
            disabled={$submitting || $allErrors.length > 0}
          >
            {$submitting ? "Signing up..." : "Sign Up"}
          </button>
        </div>
      </form>
    </div>
  </div>
{/if}
