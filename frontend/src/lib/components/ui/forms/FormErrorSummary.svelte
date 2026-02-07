<script lang="ts">
	import { XCircle } from 'phosphor-svelte';

	export type FormErrorItem = {
		path: string | Array<string | number>;
		messages: string[];
	};

	let { errors = [], title } = $props<{
		errors?: FormErrorItem[];
		title?: string;
	}>();

	function formatError(error: FormErrorItem): string {
		const message = (error?.messages ?? []).join('. ');
		const rawPath = error?.path;
		const pathParts = Array.isArray(rawPath) ? rawPath.map((p) => String(p)) : [String(rawPath ?? '')];

		if (pathParts.some((p) => p.includes('checkInRange'))) {
			return `Check-in range: ${message}`;
		}
		if (pathParts[0] === '_errors') {
			return message;
		}
		return message;
	}

	const resolvedTitle = $derived(
		title ?? `Please fix the following ${errors.length === 1 ? 'error' : 'errors'}:`
	);
</script>

{#if errors.length}
	<div class="rounded-lg border border-red-100 bg-red-50 p-4">
		<div class="flex">
			<div class="shrink-0">
				<XCircle size={22} weight="fill" class="text-red-500" />
			</div>
			<div class="ml-1">
				<h3 class="text-sm font-medium text-red-800">{resolvedTitle}</h3>
				<div class="mt-2 text-sm text-red-700">
					<ul class="list-disc space-y-1 pl-5">
						{#each errors as error}
							<li>{formatError(error)}</li>
						{/each}
					</ul>
				</div>
			</div>
		</div>
	</div>
{/if}
