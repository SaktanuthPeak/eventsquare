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
  import { formatDate } from "$lib/utils/date-utils";

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
    name?: string; // Added name property
    required?: boolean; // Added required attribute
    form?: any; // Added form property for integration with form libraries
  };

  let {
    locale = $bindable("en-GB"),
    value = $bindable(), // Now binds to ISO string
    placeholder = "Pick a date",
    formatter = df,
    onValueChange,
    name = $bindable(undefined),
    required = $bindable(false),
    form = $bindable(undefined),
  }: Props = $props();

  // Convert ISO string to DateValue for Calendar
  let calendarValue = $derived(
    value ? parseDate(new Date(value).toISOString().split("T")[0]) : undefined
  );

  // Handle Calendar changes and emit ISO string
  function handleValueChange(newValue: DateValue | undefined) {
    if (newValue) {
      const date = new Date(newValue.toString());
      date.setUTCHours(12, 0, 0, 0);
      value = date.toISOString();
      onValueChange?.(value);
    }
  }
</script>

<div>
  <Popover.Root>
    <!-- Added hidden input for form submission -->
    <input
      type="hidden"
      {name}
      {required}
      value={value || ""}
      data-form-type="date"
      aria-hidden="true"
    />

    <Popover.Trigger
      class="input cursor-pointer items-center"
      data-required={required}
    >
      <CalendarBlank class="size-5" />
      {#if value}
        {formatDate(value)}
      {:else}
        {placeholder}
      {/if}

      {#if required}
        <span class="text-red-500 ml-1">*</span>
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
