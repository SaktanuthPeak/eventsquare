<script lang="ts">
  import { page } from "$app/stores";
  import { goto } from "$app/navigation";
  import { User, SignOut, Monitor, Sparkle, Shield } from "phosphor-svelte";
  import LoginModal from "../../../../login/+page.svelte";
  import { onMount } from "svelte";

  let { orgAndUserData, UserData } = $props();

  let loggedIn = $state(false);
  let hasProfilePic = $state(false);
  let showLoginModal: boolean = $state(false);

  // hasProfilePic = Boolean(
  //   data?.user?.profile_picture || data?.user?.avatar_url
  // );

  function handleLogout() {
    goto("/logout");
  }
</script>

<div class="navbar manager-navbar">
  <div class="flex gap-[4px]">
    <!--  Logo -->
    <a href="/manager">
      <h1
        class="w-[220px] h-fit text-3xl border-none font-extrabold cursor-pointer"
      >
        EventSquare
      </h1>
    </a>

    {#if orgAndUserData?.organization_id && orgAndUserData?.orgUserData
        ?.filter((org: any) => org.id === orgAndUserData?.organization_id)
        .some((org: any) => org.role === "manager")}
      <div class="flex gap-[16px]">
        <a
          class="button bg-primary rounded-full outline-1 outline-base-100 transition-all hover:bg-[#313131] focus:bg-secondary"
          href="/manager/{orgAndUserData?.organization_id}/owner/dashboard"
        >
          <div class="flex gap-[4px]">
            <div class="flex gap-[12px] w-full">
              <div class="content-center">
                <Monitor size={16} />
              </div>
              <div>Dashboard</div>
            </div>
          </div>
        </a>

        <a
          class="button bg-primary rounded-full outline-1 outline-base-100 transition-all hover:bg-[#313131] focus:bg-secondary"
          href="/manager/{orgAndUserData?.organization_id}/owner/view-events"
        >
          <div class="flex gap-[4px]">
            <div class="flex gap-[12px] w-full">
              <div class="content-center">
                <Sparkle size={16} />
              </div>
              <div>View Events</div>
            </div>
          </div>
        </a>

        <a
          class="button bg-primary rounded-full outline-1 outline-base-100 transition-all hover:bg-[#313131] focus:bg-secondary"
          href="/manager/{orgAndUserData?.organization_id}/owner/organize-staff"
        >
          <div class="flex gap-[4px]">
            <div class="flex gap-[12px] w-full">
              <div class="content-center">
                <Shield size={16} weight="bold" />
              </div>
              <div>Organize’s Staff</div>
            </div>
          </div>
        </a>
      </div>
    {/if}
  </div>
  <div
    class="flex px-[24px] py-[12px] justify-center place-items-center content-center items-center"
  >
    {#if orgAndUserData?.user}
      <div class="flex gap-[12px] place-items-center content-center">
        <div
          class="size-[40px] rounded-full overflow-hidden flex items-center justify-center bg-neutral-content/10"
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
        <div class="w-[132px]">
          <div class="text-base-100 text-sm font-semibold line-clamp-1">
            {orgAndUserData?.user?.first_name && orgAndUserData?.user?.last_name
              ? `${orgAndUserData?.user?.first_name} ${orgAndUserData?.user?.last_name}`
              : orgAndUserData?.user?.username || "User"}
          </div>
          <div class="text-base-100 text-xs opacity-75">
            @{orgAndUserData?.user?.username || ""}
            {#if orgAndUserData?.user?.roles && orgAndUserData?.user?.roles.length > 0}
              <span class="text-xs opacity-50"
                >({orgAndUserData?.user?.roles.join(", ")})</span
              >
            {/if}
          </div>
        </div>
      </div>

      <!-- Proper SignOut button with handler -->
      <button
        onclick={handleLogout}
        class="ml-2 cursor-pointer"
        aria-label="Log out"
      >
        <SignOut size={20} class="text-neutral-content" />
      </button>
    {:else}
      <button onclick={() => (showLoginModal = true)} class="btn btn-sm">
        Login
      </button>
    {/if}
  </div>
  <LoginModal bind:showLoginModal />
</div>
