<script lang="ts">
  import { enhance } from "$app/forms";
  import { goto } from "$app/navigation";
  import { toast } from "svelte-sonner";

  let {
    show = $bindable(false),
    ticketToDelete = $bindable<{ id: string; name: string } | null>(null),
    onClose = () => {},
  } = $props();

  let isLoading = $state(false);
</script>

{#if show && ticketToDelete}
  <div class="modal modal-open">
    <div class="modal-box overflow-visible z-[50] bg-base-100 text-primary">
      <form
        method="POST"
        action="?/deleteTicket"
        use:enhance={({ formData, cancel }) => {
          isLoading = true;

          if (!ticketToDelete?.id) {
            toast.error("Invalid ticket ID");
            show = false;
            isLoading = false;
            return cancel();
          }

          return async ({ result }) => {
            isLoading = false;

            if (result.type === "success") {
              toast.success("Ticket deleted successfully");
              show = false;
              ticketToDelete = null;

              // รีโหลดหน้าเพื่อแสดงข้อมูลล่าสุด
              const url = new URL(window.location.href);
              goto(url.toString(), { invalidateAll: true, replaceState: true });
            } else {
              toast.error("Failed to delete ticket");
            }
          };
        }}
      >
        <input
          type="hidden"
          name="ticket_type_id"
          value={ticketToDelete?.id || ""}
        />

        <h3 class="font-bold text-lg">Confirm Delete</h3>
        <p class="py-4">
          Are you sure you want to delete the ticket "{ticketToDelete.name}"?
          <br />
          <span class="text-error">This action cannot be undone.</span>
        </p>
        <div class="modal-action">
          <button
            type="button"
            class="btn"
            onclick={() => {
              show = false;
              onClose();
            }}
          >
            Cancel
          </button>
          <button type="submit" class="btn btn-error" disabled={isLoading}>
            {isLoading ? "Deleting..." : "Delete"}
          </button>
        </div>
      </form>
    </div>
  </div>
{/if}
