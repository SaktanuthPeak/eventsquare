<script lang="ts">
  import { superForm } from "sveltekit-superforms";
  import type { PageData } from "./$types";
  import { toast } from "svelte-sonner";

  type Props = {
    data?: PageData;
    showCheckInModal?: boolean;
  };

  let { data, showCheckInModal = $bindable() }: Props = $props();

  const form = superForm({
    onResult: ({
      result,
    }: {
      result: { type: "success" | "error"; error?: string };
    }) => {
      if (result.type === "success") {
        toast.success("Check-in complete");
        showCheckInModal = false;
      } else if (result.type === "error") {
        console.error("Error processing QR:", result.error);
      }
    },
    dataType: "json",
  });
</script>

{#if showCheckInModal}
  <div class="modal modal-open">
    <div class="modal-box bg-base-100 text-primary p-6">
      <h3 class="font-bold text-lg">Check In EventName</h3>
      <p>Check in the user with QR code</p>
      <form method="POST">
        <button class="btn btn-primary" type="submit"> Check In </button>
      </form>
    </div>
    <!-- svelte-ignore a11y_no_static_element_interactions -->
    <!-- svelte-ignore a11y_click_events_have_key_events -->
    <div
      class="modal-backdrop"
      onclick={() => (showCheckInModal = false)}
    ></div>
  </div>
{/if}
