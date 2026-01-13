<script lang="ts">
  import SuperDebug, { superForm } from "sveltekit-superforms";
  import { zodClient } from "sveltekit-superforms/adapters";
  import { deleteEventSchema } from "./schema";
  import { goto } from "$app/navigation";
  import { toast } from "svelte-sonner";
  import TextInput from "$lib/components/ui/forms/TextInput.svelte";

  let {
    data,
    showDeleteEventModal = $bindable(),
  }: { showDeleteEventModal: boolean; data: any } = $props();

  const form = superForm(
    data.form ?? {
      eventId: "",
    },
    {
      validators: zodClient(deleteEventSchema),
      onResult: async ({ result }) => {
        console.log(result);
        if (result.type === "success") {
          showDeleteEventModal = false;
          toast.success("Event deleted successfully!");
          await goto(`/manager/${data.organization_id}/owner/view-events`);
        } else if (result.type === "failure") {
          toast.error("Failed to delete event.");
          console.error(result.data?.message || "Failed to delete event.");
        }
      },
    }
  );

  const { form: formData, enhance } = form;
  $formData.eventId = data.event_id || "";
</script>

{#if showDeleteEventModal}
  <div class="modal modal-open">
    <div class="modal-box">
      <h3 class="font-bold text-lg">Delete Event</h3>
      <p class="py-4">Are you sure you want to delete this event?</p>
      <div class="modal-action">
        <form method="POST" action="delete-event-modal" use:enhance>
          <TextInput
            {form}
            bind:value={$formData.eventId}
            name="eventId"
            type="hidden"
            placeholder="DELETE"
            required
          />
          <button
            class="btn"
            onclick={() => {
              showDeleteEventModal = false;
            }}
          >
            Cancel
          </button>
          <button class="btn btn-error" type="submit"> Delete </button>
        </form>
      </div>
    </div>
  </div>
{/if}
