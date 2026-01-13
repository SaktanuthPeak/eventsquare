<script lang="ts">
  import { X } from "phosphor-svelte";
  import type { IUser } from "$lib/models/users";
  import { goto } from "$app/navigation";
  import { zodClient } from "sveltekit-superforms/adapters";
  import { superForm } from "sveltekit-superforms/client";
  import { SignIn } from "@auth/sveltekit/components";
  import TextInput from "../../lib/components/ui/forms/TextInput.svelte";
  import { toast } from "svelte-sonner";
  import { loginSchema } from "./loginSchema";
  import SignUpModal from "../register/+page.svelte";
  import SuperDebug from "sveltekit-superforms";
  import type { PageData } from "./$types";

  let dialog: HTMLDialogElement | undefined = $state();
  let loading = $state(false);
  let error = $state("");

  type Props = {
    data?: PageData;
    showLoginModal?: boolean;
    showSignupModal?: boolean;
  };
  let {
    data,
    showLoginModal = $bindable(),
    showSignupModal = $bindable(),
  }: Props = $props();

  const form = superForm(
    data?.form ?? {
      username: "",
      password: "",
    },
    {
      validators: zodClient(loginSchema),
      onResult: async ({ result }) => {
        if (result.type === "success") {
          toast.success("Login successful!");
          showLoginModal = false;
          await goto("/manager", {
            invalidateAll: true,
          });
        } else {
          if (result.type === "failure") {
            toast.error(result.data?.errors ?? "Login failed");
          } else {
            toast.error("An unexpected error occurred");
          }
        }
      },
    }
  );

  const { form: formData, enhance } = form;
  $effect(() => {
    if (showLoginModal && dialog) dialog.showModal();
  });
</script>

{#if showLoginModal}
  <div class="modal modal-open">
    <div class="modal-box bg-base-100 flex flex-col text-primary p-6 gap-3">
      <div class="flex justify-between items-center mb-3">
        <h3 class="font-bold text-lg">Login to EventSquare</h3>
        <button
          class="btn btn-sm btn-circle btn-ghost"
          onclick={() => (showLoginModal = false)}
        >
          <X size={18} />
        </button>
      </div>

      {#if error}
        <div class="alert alert-error mb-4 text-sm text-primary">{error}</div>
      {/if}
      <form
        class="flex flex-col gap-4"
        action="/login"
        method="POST"
        use:enhance
      >
        <div class="form-control">
          <TextInput
            {form}
            bind:value={$formData.username}
            name="username"
            label="Username"
            placeholder="Enter your username"
          />
          <TextInput
            {form}
            bind:value={$formData.password}
            name="password"
            label="Password"
            type="password"
            placeholder="Enter your password"
          />
        </div>

        <div class="form-control mt-2">
          <button
            type="submit"
            class="btn btn-primary w-full"
            disabled={loading}
          >
            {loading ? "Logging in..." : "Login"}
          </button>
        </div>
      </form>

      <div>
        <span class="text-sm text-center mt-4">
          Don't have an account?{" "}
          <button
            class="text-blue-500 cursor-pointer hover:underline"
            onclick={() => ((showSignupModal = true), (showLoginModal = false))}
          >
            sign up here
          </button>
        </span>
      </div>

      <!-- <div class="text-sm text-center">
				<p class="mb-2">Use credentials:</p>
				<div class="grid grid-cols-3 gap-2 mt-2">
					<SignIn class="btn btn-sm btn-outline" provider="google" signInPage="signin" />

					<SignIn class="btn btn-sm btn-outline" provider="line" signInPage="signin" />

					<button
						class="btn btn-sm btn-outline"
						onclick={() => ((showSignupModal = true), (showLoginModal = false))}
					>
						Sign Up
					</button>
				</div>
			</div> -->
    </div>
  </div>
{/if}

<SignUpModal bind:showSignupModal />
