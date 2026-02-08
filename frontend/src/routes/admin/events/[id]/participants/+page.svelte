<script lang="ts">
    import type { PageProps } from './$types';
    import {
        ArrowLeft,
        CalendarBlank,
        Clock,
        EnvelopeSimple,
        Hash,
        Users
    } from 'phosphor-svelte';
    import { formatDateTime } from '$lib/utils/date-utils';
    import { fade } from 'svelte/transition';

    type Participant = {
        ticket_id: string;
        ticket_owner_name: string;
        quantity: number;
        email: string;
        check_in_date: Date | string;
    };

    let { data }: PageProps = $props();

    const participants = $derived((data?.participants ?? []) as Participant[]);
    const event = $derived((data?.event ?? null) as any);

    const totalCheckins = $derived(participants.length);
    const totalQuantity = $derived(participants.reduce((sum: number, item) => sum + (item.quantity ?? 0), 0));
    const latestCheckIn = $derived(
        participants.length
            ? participants
                    .map((p) =>
                        p.check_in_date instanceof Date ? p.check_in_date : new Date(p.check_in_date as any)
                    )
                    .filter((d) => !Number.isNaN(d.getTime()))
                    .sort((a, b) => b.getTime() - a.getTime())[0] ?? null
            : null
    );
    
</script>

<div class="container mx-auto px-4 py-8 space-y-6">
    <div class="flex flex-col gap-4">
        <div class="flex items-center justify-between gap-4 flex-wrap">
            <a class="btn btn-ghost gap-2" href="/admin/events">
                <ArrowLeft size={18} />
                Back
            </a>
        </div>

        <div class="space-y-1">
            <h1 class="text-2xl md:text-3xl font-bold">Checked-in Logs</h1>
            {#if event}
                <p class="text-base-content/70">
                    <span class="font-semibold">{event.name}</span>
                    {#if event.start_date && event.end_date}
                        <span class="mx-2">•</span>
                        <span>{formatDateTime(event.start_date)} – {formatDateTime(event.end_date)}</span>
                    {/if}
                </p>
            {:else}
                <p class="text-base-content/70">Event not found or not accessible.</p>
            {/if}
        </div>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4" transition:fade={{ duration: 200 }}>
        <div class="card bg-base-100 border border-base-200 shadow-sm">
            <div class="card-body p-5">
                <div class="flex items-center justify-between">
                    <div>
                        <p class="text-sm text-base-content/60">Total check-ins</p>
                        <p class="text-2xl font-bold">{totalCheckins}</p>
                    </div>
                    <div class="rounded-xl bg-primary/10 p-3">
                        <Users size={22} class="text-primary" />
                    </div>
                </div>
            </div>
        </div>
        <div class="card bg-base-100 border border-base-200 shadow-sm">
            <div class="card-body p-5">
                <div class="flex items-center justify-between">
                    <div>
                        <p class="text-sm text-base-content/60">Total quantity</p>
                        <p class="text-2xl font-bold">{totalQuantity}</p>
                    </div>
                    <div class="rounded-xl bg-secondary/10 p-3">
                        <Hash size={22} class="text-secondary" />
                    </div>
                </div>
            </div>
        </div>
        <div class="card bg-base-100 border border-base-200 shadow-sm">
            <div class="card-body p-5">
                <div class="flex items-center justify-between">
                    <div>
                        <p class="text-sm text-base-content/60">Latest check-in</p>
                        <p class="text-base font-semibold">
                            {#if latestCheckIn}
                                {formatDateTime(latestCheckIn)}
                            {:else}
                                —
                            {/if}
                        </p>
                    </div>
                    <div class="rounded-xl bg-success/10 p-3">
                        <Clock size={22} class="text-success" />
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="card bg-base-100 border border-base-200 shadow-sm">
        <div class="card-body p-5">
            <div class="flex items-center justify-between gap-3 flex-wrap">
                <div class="text-sm text-base-content/70">
                    Showing <span class="font-semibold">{participants.length}</span> check-ins
                </div>
            </div>

            {#if participants.length === 0}
                <div class="flex flex-col items-center justify-center py-12 text-center" transition:fade={{ duration: 200 }}>
                    <div class="rounded-2xl bg-base-200 p-4 mb-4">
                        <CalendarBlank size={34} class="opacity-70" />
                    </div>
                    <p class="text-lg font-semibold">No check-ins found</p>
                    <p class="text-base-content/70 max-w-md">
                        No attendees have checked in yet.
                    </p>
                </div>
            {:else}
                <!-- Desktop table -->
                <div class="hidden md:block overflow-x-auto" transition:fade={{ duration: 200 }}>
                    <table class="table table-zebra">
                        <thead>
                            <tr>
                                <th>Name</th>
                                <th>Email</th>
                                <th class="text-right">Qty</th>
                                <th>Checked in</th>
                                <th>Ticket</th>
                            </tr>
                        </thead>
                        <tbody>
                            {#each participants as p (p.ticket_id)}
                                <tr>
                                    <td class="font-medium">{p.ticket_owner_name}</td>
                                    <td>
                                        <div class="flex items-center gap-2">
                                            <EnvelopeSimple size={16} class="opacity-70" />
                                            <span class="truncate max-w-[320px]">{p.email}</span>
                                        </div>
                                    </td>
                                    <td class="text-right"><span class="badge badge-ghost">{p.quantity}</span></td>
                                    <td>{formatDateTime(p.check_in_date)}</td>
                                    <td>
                                        <span class="font-mono text-xs opacity-80">{p.ticket_id}</span>
                                    </td>
                                </tr>
                            {/each}
                        </tbody>
                    </table>
                </div>

                <!-- Mobile cards -->
                <div class="md:hidden grid grid-cols-1 gap-3" transition:fade={{ duration: 200 }}>
                    {#each participants as p (p.ticket_id)}
                        <div class="card bg-base-100 border border-base-200">
                            <div class="card-body p-4">
                                <div class="flex items-start justify-between gap-3">
                                    <div class="min-w-0">
                                        <p class="font-semibold truncate">{p.ticket_owner_name}</p>
                                        <p class="text-sm opacity-70 truncate">{p.email}</p>
                                    </div>
                                    <span class="badge badge-ghost">Qty {p.quantity}</span>
                                </div>

                                <div class="mt-3 flex items-center gap-2 text-sm">
                                    <Clock size={16} class="opacity-70" />
                                    <span>{formatDateTime(p.check_in_date)}</span>
                                </div>
                                <div class="mt-2">
                                    <span class="font-mono text-xs opacity-70 break-all">{p.ticket_id}</span>
                                </div>
                            </div>
                        </div>
                    {/each}
                </div>
            {/if}
        </div>
    </div>
</div>
