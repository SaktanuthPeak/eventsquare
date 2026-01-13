<script lang="ts">
  import { onMount } from "svelte";
  import { page } from "$app/stores";
  import { goto } from "$app/navigation";
  import GuestNavbar from "./guestNav/+page.svelte";
  import LoginModal from "./login/+page.svelte";
  import SignupModal from "./register/+page.svelte";

  import {
    CalendarDots,
    Users,
    ChartBar,
    CheckCircle,
    ArrowRight,
  } from "phosphor-svelte";
  import Footer from "$lib/components/footer/manager-footer.svelte";

  let showLoginModal = $state(false);
  let showSignupModal = $state(false);

  // Features section data
  const features = [
    {
      icon: CalendarDots,
      title: "Event Management",
      description:
        "Create and manage multiple events with an intuitive dashboard",
    },
    {
      icon: Users,
      title: "Staff Organization",
      description:
        "Assign roles to your team members and track their responsibilities",
    },
    {
      icon: ChartBar,
      title: "Analytics",
      description:
        "Get real-time insights into ticket sales, attendance, and more",
    },
  ];

  // Testimonials data
  const testimonials = [
    {
      quote:
        "EventSquare has transformed how we organize our music festivals. The platform is intuitive and powerful.",
      author: "Sarah Johnson",
      role: "Event Director, SoundWave Festival",
    },
    {
      quote:
        "The analytics dashboard gives us real-time insights we never had before. Our events are now more profitable than ever.",
      author: "Michael Chen",
      role: "CEO, Conference Connect",
    },
  ];

  // Check if user is already logged in
  onMount(() => {
    if ($page.data.user) {
      const role = $page.data.user.roles?.[0] || $page.data.user.role;
      if (role === "admin") {
        goto("/admin");
      } else if (role === "manager") {
        goto("/manager");
      } else {
        goto("/");
      }
    }
  });
</script>

<div class="min-h-screen bg-base-100">
  <GuestNavbar />
  <!-- Hero Section -->
  <section
    class="relative bg-gradient-to-br from-primary to-primary-focus text-primary-content py-20"
  >
    <div class="container mx-auto px-6 py-16 text-center">
      <h1 class="text-5xl font-bold mb-6">Organize Events with Confidence</h1>
      <p class="text-xl mb-8 max-w-2xl mx-auto">
        EventSquare gives you the tools to manage, organize, and scale your
        events with ease.
      </p>
      <div class="flex justify-center gap-4">
        <button
          class="btn botton btn-secondary btn-lg"
          onclick={() => (showSignupModal = true)}
        >
          Get Started
          <ArrowRight size={18} />
        </button>
        <button
          class="btn btn-outline btn-lg border-primary-content text-primary-content hover:bg-primary-focus"
          onclick={() => (showLoginModal = true)}
        >
          Log In
        </button>
      </div>
    </div>
  </section>

  <!-- Features Section -->
  <section class="py-20 bg-base-100">
    <div class="container mx-auto px-6">
      <h2 class="text-3xl font-bold text-center mb-12">
        Powerful Features for Event Organizers
      </h2>

      <div class="grid md:grid-cols-3 gap-10">
        {#each features as feature}
          <div class="card bg-base-200 hover:shadow-lg transition-all">
            <div class="card-body">
              <div
                class="bg-primary text-primary-content p-3 rounded-full w-12 h-12 flex items-center justify-center mb-4"
              ></div>
              <h3 class="card-title text-xl font-semibold">{feature.title}</h3>
              <p class="text-base-content/80">{feature.description}</p>
            </div>
          </div>
        {/each}
      </div>
    </div>
  </section>

  <!-- Dashboard Preview Section -->
  <section class="py-20 bg-base-200">
    <div class="container mx-auto px-6">
      <div class="flex flex-col md:flex-row items-center gap-10">
        <div class="md:w-1/2">
          <h2 class="text-3xl font-bold mb-6">
            Intuitive Dashboard for Total Control
          </h2>
          <p class="text-lg mb-8">
            Our powerful dashboard gives event managers and administrators
            complete visibility and control over every aspect of their events.
          </p>
          <ul class="space-y-4">
            {#each ["Real-time attendee tracking", "Staff management and assignments", "Ticket sales monitoring", "Custom event pages and branding"] as benefit}
              <li class="flex items-start gap-2">
                <CheckCircle
                  class="text-secondary mt-1 flex-shrink-0"
                  size={20}
                />
                <span>{benefit}</span>
              </li>
            {/each}
          </ul>
          <button
            class="btn btn-primary mt-8"
            onclick={() => (showSignupModal = true)}
          >
            Try It Now
          </button>
        </div>
        <div class="md:w-1/2 relative">
          <div class="relative z-10 rounded-lg shadow-xl overflow-hidden">
            <img
              src="https://placehold.co/800x500/1a1a1a/FFFFFF?text=Dashboard+Preview"
              alt="EventSquare Dashboard"
              class="w-full"
            />
          </div>
          <div
            class="absolute -bottom-6 -right-6 w-80 h-80 bg-secondary/20 rounded-full filter blur-3xl -z-10"
          ></div>
        </div>
      </div>
    </div>
  </section>

  <!-- Testimonials Section -->
  <section class="py-20 bg-base-100">
    <div class="container mx-auto px-6">
      <h2 class="text-3xl font-bold text-center mb-12">
        What Event Organizers Say
      </h2>

      <div class="grid md:grid-cols-2 gap-8">
        {#each testimonials as testimonial}
          <div class="card bg-base-200 border-t-4 border-secondary">
            <div class="card-body">
              <div class="text-3xl text-secondary mb-4">"</div>
              <p class="text-lg italic mb-6">{testimonial.quote}</p>
              <div class="flex items-center">
                <div class="w-12 h-12 bg-primary rounded-full mr-4"></div>
                <div>
                  <h4 class="font-bold">{testimonial.author}</h4>
                  <p class="text-sm text-base-content/70">{testimonial.role}</p>
                </div>
              </div>
            </div>
          </div>
        {/each}
      </div>
    </div>
  </section>

  <!-- CTA Section -->
  <section class="py-16 bg-primary text-primary-content">
    <div class="container mx-auto px-6 text-center">
      <h2 class="text-3xl font-bold mb-6">
        Ready to Transform Your Event Management?
      </h2>
      <p class="text-xl mb-8 max-w-2xl mx-auto">
        Join thousands of event organizers who trust EventSquare for their
        events.
      </p>
      <div class="flex justify-center gap-4">
        <button
          class="btn btn-secondary btn-lg"
          onclick={() => (showSignupModal = true)}
        >
          Sign Up Free
        </button>
        <button
          class="btn btn-outline btn-lg border-primary-content text-primary-content hover:bg-primary-focus"
          onclick={() => (showLoginModal = true)}
        >
          Log In
        </button>
      </div>
    </div>
  </section>

  <Footer />

  <!-- Modals -->
  <LoginModal bind:showLoginModal />
  <SignupModal bind:showSignupModal />
</div>
