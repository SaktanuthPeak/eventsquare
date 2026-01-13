<script lang="ts">
  import { cn } from "$lib/utils/tw-utils";
  import { Popover } from "bits-ui";
  import type { Snippet } from "svelte";
  import type { ComponentProps } from "svelte";

  type Props = {
    children: Snippet;
    trigger?: Snippet;
    open?: boolean;
    triggerClass?: string;
  };

  let {
    children,
    trigger,
    open = $bindable(false),
    triggerClass,
    ...restProps
  }: ComponentProps<typeof Popover.Content> & Props = $props();
</script>

<Popover.Root bind:open>
  <Popover.Trigger class={cn("btn", triggerClass)}>
    {#if trigger}
      {@render trigger()}
    {:else}
      Open
    {/if}
  </Popover.Trigger>
  <Popover.Portal>
    <Popover.Content {...restProps}>
      {@render children()}
    </Popover.Content>
  </Popover.Portal>
</Popover.Root>
