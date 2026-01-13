<script lang="ts">
  import { SignOut } from "phosphor-svelte";
  import LoginModal from "../login/+page.svelte";
  import SignupModal from "../register/+page.svelte";
  let showLoginModal: boolean = $state(false);
  let showSignupModal: boolean = $state(false);
</script>

<div class="navbar admin-navbar">
  <div class="flex gap-[4px]">
    <!--  Logo -->
    <a href="/">
      <h1 class="w-[220px] h-fit text-3xl font-extrabold cursor-pointer">
        EventSquare
      </h1>
    </a>
  </div>
  <!-- {#if isAuthenticated && user} -->
  <div class="hidden lg:show">
    <div
      class=" lg:show flex px-[24px] py-[12px] justify-center place-items-center content-center items-center"
    >
      <div class="flex gap-[12px] place-items-center content-center">
        <div
          class="size-[40px] rounded-full overflow-hidden flex items-center justify-center"
        >
          <img
            src={""}
            alt="Profile_picture"
            class="w-full h-full object-cover"
          />
        </div>
        <div class="w-[132px]">
          <!-- <div class="text-base-100 text-sm font-semibold line-clamp-1">
              {user.first_name
                ? `${user.first_name} ${user.last_name}`
                : user.username || user.email}
            </div>
            <div class="text-base-100 text-xs">
              @{user.roles ? user.roles.join(", ") : user.role || "user"}
            </div> -->
        </div>
      </div>
      <button class="ml-2 cursor-pointer" aria-label="Log out">
        <SignOut size={20} />
      </button>
    </div>
  </div>
  <!-- {:else} -->
  <div class="flex gap-[10px]">
    <div class="flex gap-[12px]">
      <button
        class="login-navbar-button"
        onclick={() => (showLoginModal = true)}
      >
        <div class="font-bold">Login</div>
      </button>
    </div>
    <div class="flex gap-[12px]">
      <button
        class="login-navbar-button"
        onclick={() => (showSignupModal = true)}
      >
        <div class="font-bold">Sign Up</div>
      </button>
    </div>
  </div>
  <LoginModal bind:showLoginModal />
  <SignupModal bind:showSignupModal />
  <!-- {/if} -->
</div>

<style>
</style>
