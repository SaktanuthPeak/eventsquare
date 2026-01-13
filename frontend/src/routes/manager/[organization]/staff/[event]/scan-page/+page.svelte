<script lang="ts">
  import { onDestroy, onMount } from "svelte";
  import { Html5Qrcode } from "html5-qrcode";
  import type { PageData } from "./$types";
  import SuperDebug, { superForm } from "sveltekit-superforms";
  import { zodClient } from "sveltekit-superforms/adapters";
  import { scanPageSchema } from "./schema";
  import TextInput from "$lib/components/ui/forms/TextInput.svelte";
  import CheckInModal from "./check-in-modal/+page.svelte";

  let { data }: { data: PageData } = $props();
  let html5QrCode: Html5Qrcode;
  let scanning = $state(false);
  let showCheckInModal: boolean = $state(false);

  const form = superForm(data.form, {
    validators: zodClient(scanPageSchema),
    onResult: ({ result }) => {
      // Handle server response
      if (result.type === "success") {
        console.log("QR processed successfully");
        showCheckInModal = true;
      } else if (result.type === "error") {
        console.error("Error processing QR:", result.error);
      }
    },
  });

  const { form: formData, enhance } = form;

  onMount(async () => {
    html5QrCode = new Html5Qrcode("qr-reader");
    startScanning();
  });

  onDestroy(() => {
    if (html5QrCode && scanning) {
      html5QrCode.stop();
    }
  });

  async function startScanning() {
    try {
      scanning = true;
      await html5QrCode.start(
        { facingMode: "environment" },
        {
          fps: 10,
          qrbox: { width: 450, height: 450 },
        },
        onScanSuccess,
        (error) => console.error("QR Code scanning error:", error)
      );
    } catch (error) {
      console.error("Error starting scanner:", error);
      scanning = false;
    }
  }

  async function onScanSuccess(decodedText: string) {
    try {
      html5QrCode.pause(); // Pause scanning
      $formData.qrCode = decodedText;
    } catch (error) {
      console.error("Error processing QR code:", error);
    }
  }

  function resumeScanning() {
    html5QrCode.resume();
  }
</script>

<div class="flex flex-col items-center justify-center h-screen">
  <h1 class="text-2xl font-bold mb-4">Scan QR Code</h1>

  <div
    id="qr-reader"
    class="w-full h-[500px] rounded-4xl max-w-3xl border-2 border-gray-300 overflow-hidden"
  ></div>

  <form method="POST" use:enhance class="mt-4 flex flex-col items-center gap-4">
    <p class="text-gray-600 text-center">
      Position the QR code within the frame to scan
    </p>
    <TextInput
      {form}
      bind:value={$formData.qrCode}
      type="hidden"
      name="qrCode"
      placeholder="Scanned QR Code"
      required
    />
    {#if $formData.qrCode}
      <div class="flex flex-row my-2 gap-4">
        <button class="btn btn-primary" type="submit"> Verify QR Code </button>
        <button type="button" class="btn btn-outline" onclick={resumeScanning}>
          Scan Again
        </button>
      </div>
    {/if}
  </form>

  <div class="flex flex-col gap-2 items-center p-[5px]">
    <button class="btn btn-primary" onclick={resumeScanning}>
      Resume Scanning
    </button>

    <!-- <SuperDebug data={$formData} /> -->
  </div>
</div>

<CheckInModal bind:showCheckInModal />

<style>
  :global(#qr-reader) {
    width: 100% !important;
    min-height: 300px;
  }

  :global(#qr-reader video) {
    width: 100% !important;
    border-radius: 0.5rem;
  }
</style>
