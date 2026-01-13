<script lang="ts">
  import { onMount } from "svelte";
  import type { PageData } from "./$types";
  import Qrcode from "$lib/components/ui/QRJS.svelte";
  import html2canvas from "html2canvas-pro";
  import { jsPDF } from "jspdf";
  import { env } from "$env/dynamic/public";

  let {
    showGetCheckInQrModal = $bindable(),
    data,
  }: { showGetCheckInQrModal: boolean; data: PageData } = $props();

  let qrCodeElement: HTMLDivElement | null = $state(null);
  let checkInQrcode = `${env.PUBLIC_FRONTEND_URL}/events/${data.event_id}/check-in`;

  async function downloadAsPDF() {
    if (!qrCodeElement) return;
    const canvas = await html2canvas(qrCodeElement);
    const imgData = canvas.toDataURL("image/png");
    const pdf = new jsPDF({
      orientation: "portrait",
      unit: "mm",
      format: "a4",
    });
    const margin = 40;

    const pdfWidth = pdf.internal.pageSize.getWidth();
    const pdfHeight = pdf.internal.pageSize.getHeight();

    const imageWidth = canvas.width;
    const imageHeight = canvas.height;

    const avaliableWidth = pdfWidth - margin * 2;
    const avaliableHeight = pdfHeight - margin * 2;

    const ratio = Math.min(
      avaliableWidth / imageWidth,
      avaliableHeight / imageHeight
    );

    const displayWidth = imageWidth * ratio;
    const displayHeight = imageHeight * ratio;

    const centerX = (pdfWidth - displayWidth) / 2;
    const centerY = (pdfHeight - displayHeight) / 2;

    pdf.addImage(imgData, "PNG", centerX, centerY, displayWidth, displayHeight);
    pdf.save("qrcode.pdf");
  }

  async function downloadAsImage() {
    try {
      if (!qrCodeElement) return;
      const canvas = await html2canvas(qrCodeElement, {
        scale: 2,
        useCORS: true,
      });

      const link = document.createElement("a");
      link.download = `qrcode-${Date.now()}.png`;
      link.href = canvas.toDataURL("image/png");
      link.click();
      document.body.removeChild(link);
    } catch (error) {
      console.error("Error downloading QR code as image:", error);
    }
  }
</script>

{#if showGetCheckInQrModal}
  <div class="modal modal-open">
    <div class="modal-box">
      <div class="flex flex-col items-center">
        <h2 class="font-bold text-xl">Get Check-In QR Code</h2>
        <button
          class="btn btn-sm btn-circle absolute right-2 top-2"
          onclick={() => (showGetCheckInQrModal = false)}>✕</button
        >
        <div bind:this={qrCodeElement} id="qrCodeElement">
          <h1 class="text-4xl font-bold text-center pb-2">
            {data.eventData?.title}
          </h1>
          <div id="qrcode" class="flex justify-center">
            <Qrcode codeValue={checkInQrcode} squareSize="500" />
          </div>
        </div>
        <button class="btn btn-secondary w-full my-5" onclick={downloadAsPDF}>
          Download PDF
        </button>
        <button class="btn btn-primary w-full" onclick={downloadAsImage}>
          Download Image
        </button>
      </div>
    </div>
  </div>
{/if}
