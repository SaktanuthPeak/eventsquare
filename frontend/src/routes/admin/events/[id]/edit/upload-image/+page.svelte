<script lang="ts">
    import type { PageData } from './$types';
    import { env } from '$env/dynamic/public';
    import { fileProxy, superForm } from 'sveltekit-superforms';
    import { zodClient } from 'sveltekit-superforms/adapters';
    import { imageUploadSchema } from '$lib/schemas/imageUploadSchema';
    import FileInput from '$lib/components/ui/forms/FileInput.svelte';
    import FormErrorSummary from '$lib/components/ui/forms/FormErrorSummary.svelte';
    import { toast } from 'svelte-sonner';
    import { goto, invalidateAll } from '$app/navigation';

    let { data }: { data: PageData } = $props();

    const event = $derived(data.event);

    const uploadForm = $derived.by(() =>
        superForm(data.form as any, {
            validators: zodClient(imageUploadSchema as any),
            customValidity: true,
            dataType: 'form',
            onResult: async ({ result }) => {
                if (result.type === 'success') {
                    toast.success('Image uploaded');
                    await invalidateAll();
                    if (event?.id) {
                        await goto(`/admin/events/${event.id}/edit`, { invalidateAll: true });
                    }
                } else if (result.type === 'failure') {
                    toast.error((result.data as any)?.message || 'Image upload failed');
                }
            }
        })
    );

    const enhance = $derived(uploadForm.enhance);
    const allErrors = $derived(uploadForm.allErrors);
    const submitting = $derived(uploadForm.submitting);
    const file = $derived(fileProxy(uploadForm, 'image'));

    const apiBase = $derived(env.PUBLIC_API_URL || env.PUBLIC_BASE_API_URL || 'http://localhost:9000');
    const currentImageUrl = $derived(
        event?.image_id ? `${apiBase}/v1/images/${event.image_id}` : null
    );
</script>

<div class="container mx-auto px-4 py-10">
    <div class="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div>
            <h1 class="text-2xl font-bold">Upload event image</h1>
            <p class="mt-1 text-base-content/70">
                {#if event}{event.name}{:else}Event{/if} — upload/replace the cover image.
            </p>
        </div>
        <div class="flex gap-2">
            <a class="btn btn-ghost" href="/admin/events">Back</a>
            {#if event}
                <a class="btn btn-outline" href={`/admin/events/${event.id}/edit`}>Edit event</a>
                <a class="btn btn-outline" href={`/admin/events/${event.id}/tickets`}>Tickets</a>
            {/if}
        </div>
    </div>

    {#if !event}
        <div class="mt-8 alert alert-error">Event not found.</div>
    {:else}
        <div class="mt-8 grid gap-6 lg:grid-cols-2">
            <div class="rounded-lg border border-base-200 bg-base-100 p-6">
                <h2 class="text-xl font-bold">Current image</h2>
                <p class="mt-1 text-sm text-base-content/70">If you upload a new image, it will replace this.</p>
                <div class="mt-4 overflow-hidden rounded-lg border border-base-200 bg-base-200">
                    {#if currentImageUrl}
                        <img
                            src={currentImageUrl}
                            alt="Event cover"
                            class=" w-full object-cover"
                            loading="lazy"
                        />
                    {:else}
                        <div class="flex h-56 items-center justify-center text-sm text-base-content/60">
                            No image uploaded yet.
                        </div>
                    {/if}
                </div>
            </div>

            <div class="rounded-lg border border-base-200 bg-base-100 p-6">
                <h2 class="text-xl font-bold">Upload a new image</h2>
                <p class="mt-1 text-sm text-base-content/70">Supported: JPEG/PNG/WebP. Recommended 16:9.</p>

                <form
                    method="POST"
                    enctype="multipart/form-data"
                    use:enhance
                    class="mt-4 space-y-3"
                >
                    <FileInput
                        form={uploadForm}
                        bind:files={$file}
                        name="image"
                        label="Event image"
                        description="Choose an image file"
                    />
                    <FormErrorSummary errors={$allErrors} />
                    <button type="submit" class="btn btn-primary w-full" disabled={$submitting}>
                        {$submitting ? 'Uploading...' : 'Upload image'}
                    </button>
                </form>
            </div>
        </div>
    {/if}
</div>