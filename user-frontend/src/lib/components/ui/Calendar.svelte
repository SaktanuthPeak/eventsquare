<script lang="ts">
  import { Calendar } from "bits-ui";
  import {
    DateFormatter,
    getLocalTimeZone,
    today,
    type DateValue,
    parseDate,
  } from "@internationalized/date";
  import CaretLeft from "phosphor-svelte/lib/CaretLeft";
  import CaretRight from "phosphor-svelte/lib/CaretRight";
  import { date } from "zod";

  const currentDate = today(getLocalTimeZone());
  const currentYear = new Date().getFullYear();
  const yearList = Array.from({ length: 30 }, (_, i) => currentYear - i);

  type Props = {
    locale?: string;
    value?: DateValue;
    placeholder?: DateValue;
    selectableYears?: number[];
    selectable?: boolean;
    onValueChange?: (value: DateValue | undefined) => void;
  };
  let {
    locale = $bindable("en-GB"),
    value = $bindable(),
    placeholder = $bindable(currentDate),
    selectableYears = yearList,
    selectable = false,
    onValueChange,
  }: Props = $props();

  const formatter = new DateFormatter(locale, {
    month: "long",
    year: "numeric",
  });
</script>

<Calendar.Root
  class="border-dark-10 bg-background-alt shadow-card mt-6 rounded-[15px] border p-[22px]"
  weekdayFormat="short"
  fixedWeeks={true}
  type="single"
  bind:value
  minValue={today(getLocalTimeZone())}
  {onValueChange}
>
  {#snippet children({ months, weekdays })}
    <Calendar.Header class="flex items-center justify-between">
      <Calendar.PrevButton
        class="rounded-9px bg-background-alt hover:bg-muted inline-flex size-10 items-center justify-center active:scale-[0.98] active:transition-all"
      >
        <CaretLeft class="size-6" />
      </Calendar.PrevButton>
      <Calendar.Heading class="text-[15px] font-medium" />
      <Calendar.NextButton
        class="rounded-9px bg-background-alt hover:bg-muted inline-flex size-10 items-center justify-center active:scale-[0.98] active:transition-all"
      >
        <CaretRight class="size-6" />
      </Calendar.NextButton>
    </Calendar.Header>
    <div
      class="flex flex-col space-y-4 pt-4 sm:flex-row sm:space-x-4 sm:space-y-0"
    >
      {#each months as month, i (i)}
        <Calendar.Grid class="w-full border-collapse select-none space-y-1">
          <Calendar.GridHead>
            <Calendar.GridRow class="mb-1 flex w-full justify-between">
              {#each weekdays as day}
                <Calendar.HeadCell
                  class="text-muted-foreground font-normal! w-10 rounded-md text-xs"
                >
                  <div>{day.slice(0, 2)}</div>
                </Calendar.HeadCell>
              {/each}
            </Calendar.GridRow>
          </Calendar.GridHead>
          <Calendar.GridBody>
            {#each month.weeks as weekDates}
              <Calendar.GridRow class="flex w-full">
                {#each weekDates as date}
                  <Calendar.Cell
                    {date}
                    month={month.value}
                    class="p-0! relative size-10 text-center text-sm"
                  >
                    <Calendar.Day
                      class={[
                        "rounded-md",
                        "relative inline-flex size-10 items-center justify-center",
                        "text-sm font-normal",
                        "border border-transparent",
                        "transition-colors",
                        //date selected
                        "data-selected:bg-black/10",
                        // Base styles
                        "text-foreground hover:bg-muted/50",
                        // Today's date
                        "data-[today]:bg-accent/20",
                        // Disabled state
                        "data-[disabled]:pointer-events-none data-[disabled]:opacity-50",
                        // Outside month
                        "data-[outside-month]:pointer-events-none data-[outside-month]:text-muted-foreground/50",
                        // Unavailable dates
                        "data-[unavailable]:line-through data-[unavailable]:text-muted-foreground",
                      ].join(" ")}
                    >
                      <div
                        class="absolute top-[5px] left-1/2 -translate-x-1/2 size-1 rounded-full data-[today]:bg-primary"
                      ></div>

                      {date.day}
                    </Calendar.Day>
                  </Calendar.Cell>
                {/each}
              </Calendar.GridRow>
            {/each}
          </Calendar.GridBody>
        </Calendar.Grid>
      {/each}
    </div>
  {/snippet}
</Calendar.Root>
