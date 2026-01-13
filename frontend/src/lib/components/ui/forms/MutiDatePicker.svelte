<script lang="ts">
  import { Popover } from "bits-ui";
  import Calendar from "../Calendar.svelte";
  import {
    CalendarDateTime,
    DateFormatter,
    getLocalTimeZone,
    parseDate,
    type DateValue,
  } from "@internationalized/date";
  import CalendarBlank from "phosphor-svelte/lib/CalendarBlank";
  import { X } from "phosphor-svelte";

  const df = new DateFormatter("en-GB", {
    dateStyle: "short",
  });

  type Props = {
    locale?: string;
    values?: string[]; // Now expects ISO list instead of DateValue
    placeholder?: string;
    formatter?: DateFormatter;
    selectableYears?: number[];
    selectable?: boolean;
    onValuesChange?: (value: string[] | undefined) => void; // Emits ISO string
    name?: string; // Added name property
    required?: boolean; // Added required attribute
    form?: any; // Added form property for form libraries
  };

  let {
    locale = $bindable("en-GB"),
    values = $bindable([]), // Initialize with empty array
    placeholder = "Pick a date",
    formatter = df,
    onValuesChange,
    name = $bindable(undefined),
    required = $bindable(false),
    form = $bindable(undefined),
  }: Props = $props();

  // Convert ISO string to DateValue for Calendar
  let calendarValue = $state<DateValue | undefined>(undefined);

  // Handle Calendar changes and emit ISO string
  function handleValueChange(newValue: DateValue | undefined) {
    if (newValue) {
      const isoString = newValue.toString();

      // Add to values if not already present
      if (!values?.includes(isoString)) {
        const newValues = [...(values || []), isoString].sort();
        values = newValues;
        onValuesChange?.(newValues);
      }

      // Reset calendar selection
      calendarValue = undefined;
    }
  }

  function removeDate(dateToRemove: string) {
    const newValues = values?.filter((d) => d !== dateToRemove);
    values = newValues;
    onValuesChange?.(newValues);
  }
</script>

<div class="w-full space-y-2">
  <!-- Added hidden input field for form submission -->
  <input
    type="hidden"
    {name}
    {required}
    value={values?.join(",")}
    data-form-type="multi-date"
    aria-hidden="true"
  />

  <Popover.Root>
    <Popover.Trigger
      class="input cursor-pointer items-center w-full"
      data-required={required}
    >
      <CalendarBlank class="size-5" />
      {#if values?.length > 0}
        <span class="ml-2">{values.length} dates selected</span>
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
          {locale}
          value={calendarValue}
          onValueChange={handleValueChange}
        />
      </Popover.Content>
    </Popover.Portal>
  </Popover.Root>

  {#if values.length > 0}
    <div class="flex flex-wrap gap-2">
      {#each values as date (date)}
        <div class="badge badge-lg gap-2 bg-primary/10">
          {formatter.format(new Date(date))}
          <button
            type="button"
            class="btn btn-ghost btn-xs p-0"
            onclick={() => removeDate(date)}
          >
            <X size={14} />
          </button>
        </div>
      {/each}
    </div>
  {/if}
</div>
