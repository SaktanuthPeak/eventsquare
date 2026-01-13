<script lang="ts">
  import type { PageData } from "./$types";

  type Props = {
    data: PageData;
    showAddStaffModal?: boolean;
  };

  let { data, showAddStaffModal = $bindable() }: Props = $props();
</script>

{#if showAddStaffModal}
  <div class="modal modal-open">
    <div class="modal-box">
      <h3 class="font-bold text-xl">Add New Staff</h3>
      <p class="py-4">Staff addition form goes here</p>
      <div class="modal-action">
        <button class="btn" onclick={() => (showAddStaffModal = false)}
          >Close</button
        >
        <button class="btn btn-primary">Save</button>
      </div>
    </div>
    <div
      class="modal-backdrop"
      onclick={() => (showAddStaffModal = false)}
    ></div>
  </div>
{/if}
