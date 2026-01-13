<script lang="ts">
  import { Popover, Portal } from "bits-ui";
  import Calendar from "../Calendar.svelte";
  import {
    CalendarDateTime,
    DateFormatter,
    getLocalTimeZone,
    parseDate,
    type DateValue,
  } from "@internationalized/date";
  import CalendarBlank from "phosphor-svelte/lib/CalendarBlank";

  const df = new DateFormatter("en-GB", {
    dateStyle: "short",
  });

  type Props = {
    locale?: string;
    value?: string; // Now expects ISO string instead of DateValue
    placeholder?: string;
    formatter?: DateFormatter;
    selectableYears?: number[];
    selectable?: boolean;
    onValueChange?: (value: string | undefined) => void; // Emits ISO string
  };

  let {
    locale = $bindable("en-GB"),
    value = $bindable(), // Now binds to ISO string
    placeholder = "Pick a date",
    formatter = df,
    onValueChange,
  }: Props = $props();

  // Convert ISO string to DateValue for Calendar
  let calendarValue = $derived(
    value ? parseDate(new Date(value).toISOString().split("T")[0]) : undefined
  );

  // Handle Calendar changes and emit ISO string
  function handleValueChange(newValue: DateValue | undefined) {
    const isoString = newValue?.toDate(getLocalTimeZone()).toISOString();
    value = isoString; // Update bound value
    onValueChange?.(isoString); // Notify parent
  }
</script>

<div>
  <Popover.Root>
    <Popover.Trigger class="input cursor-pointer items-center">
      <CalendarBlank class="size-5" />
      {#if value}
        {formatter.format(new Date(value))}
        <!-- Display formatted ISO string -->
      {:else}
        {placeholder}
      {/if}
    </Popover.Trigger>
    <Popover.Portal>
      <Popover.Content class="bits-popover-content">
        <Calendar
          bind:locale
          bind:value={calendarValue}
          onValueChange={handleValueChange}
        />
      </Popover.Content>
    </Popover.Portal>
  </Popover.Root>
</div>
