<script lang="ts">
  import { User } from "phosphor-svelte";
  import type { PageData } from "./$types";

  let { orgNavData }: { data: PageData } = $props();
</script>

<nav
  class="navbar h-[100px] flex gap-[75px] mt-[15px] mb-[25px] items-center bg-base-200 px-[250px]"
>
  <div
    class="size-[48px] rounded-full overflow-hidden flex items-center justify-center bg-neutral-content/10"
  >
    <!-- {#if hasProfilePic}
            <img
              src={data?.user?.profile_picture || data?.user?.avatar_url}
              alt="Profile"
              class="w-full h-full object-cover"
            />
          {:else} -->
    <User size={24} weight="bold" class="text-neutral-content" />
    <!-- {/if} -->
  </div>
  <div class="">
    <h1 class="text-lg font-bold text-base-content">
      {orgNavData?.orgData?.organizer.name || "Organization Name"}
    </h1>
    <a
      href="/manager/{orgNavData?.organization_id}/owner/edit-organization?id={encodeURIComponent(
        orgNavData?.orgData?.organizer.id
      )}"
    >
      <p class="text-sm text-base-content/70">Edit organization</p>
    </a>
  </div>
</nav>
