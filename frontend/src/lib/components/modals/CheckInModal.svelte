<script lang="ts">
  import { superForm } from "sveltekit-superforms";
  import type { createEventSchema } from "../../../routes/manager/[organization]/owner/view-events/create-event/schema";
  import DatePicker from "../ui/forms/DatePicker.svelte";

  let {
    form,
    showCheckInRangeModal = $bindable(),
    onSave,
  } = $props<{
    form: ReturnType<typeof superForm<typeof createEventSchema>>;
    showCheckInRangeModal?: boolean;
    onSave: (range: { start_time: string; end_time: string }) => void;
  }>();

  let startDate = $state<string>("");
  let startTime = $state<string>("");
  let endDate = $state<string>("");
  let endTime = $state<string>("");

  function handleSubmit() {
    if (!startDate || !startTime || !endDate || !endTime) {
      console.log("Missing required fields");
      return;
    }

    // Parse start date and time
    const [startHours, startMinutes] = startTime.split(":").map(Number);
    const startDateTime = new Date(startDate);
    startDateTime.setHours(startHours, startMinutes, 0, 0);
    // Parse end date and time
    const [endHours, endMinutes] = endTime.split(":").map(Number);
    const endDateTime = new Date(endDate);
    endDateTime.setHours(endHours, endMinutes, 0, 0);

    const startDateTimeIso = startDateTime.toISOString();
    const endDateTimeIso = endDateTime.toISOString();

    if (startDateTimeIso && endDateTimeIso) {
      onSave({
        start_time: startDateTimeIso,
        end_time: endDateTimeIso,
      });
      showCheckInRangeModal = false;

      // Reset form
      startDate = "";
      startTime = "";
      endDate = "";
      endTime = "";
    }
  }
</script>

{#if showCheckInRangeModal}
  <div class="modal modal-open">
    <div class="modal-box max-w-l">
      <h3 class="font-bold text-lg mb-4">Add Check-in Time Range</h3>

      <div class="w-full space-y-4">
        <!-- Start Time Row -->
        <div class="flex gap-4 items-end">
          <div class="flex-1">
            <label class="label">Start Time</label>
            <DatePicker
              locale="en-GB"
              bind:value={startDate}
              placeholder="Select Date"
              name="start_time"
              required
            />
          </div>
          <div class="w-[120px]">
            <!-- Fixed width for time input -->
            <input
              type="time"
              class="input input-bordered w-full"
              bind:value={startTime}
            />
          </div>
        </div>

        <!-- End Time Row -->
        <div class="flex gap-4 items-end">
          <div class="flex-1">
            <label class="label">End Time</label>
            <DatePicker
              locale="en-GB"
              bind:value={endDate}
              placeholder="Select Date"
              name="end_time"
              required
            />
          </div>
          <div class="w-[120px]">
            <input
              type="time"
              class="input input-bordered w-full"
              bind:value={endTime}
            />
          </div>
        </div>
      </div>

      <div class="modal-action">
        <button class="btn" onclick={() => (showCheckInRangeModal = false)}
          >Cancel</button
        >
        <button
          class="btn btn-primary"
          onclick={handleSubmit}
          disabled={!startTime || !endTime}
        >
          Add Range
        </button>
      </div>
    </div>
  </div>
{/if}
