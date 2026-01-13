<script lang="ts">
	import { User, Envelope, At, Calendar, PencilSimple } from 'phosphor-svelte';
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();

	// Sample joined date (replace with actual data if available)
	const joinedDate = new Date().toLocaleDateString('en-US', {
		year: 'numeric',
		month: 'long',
		day: 'numeric'
	});
</script>

<div class="flex flex-col w-full h-full">
	<!-- Profile Header-->
	<div class="bg-gradient-to-r from-primary/10 to-secondary/10 rounded-xl p-8 mb-6">
		<div class="flex flex-col md:flex-row items-center gap-6">
			<!-- Profile Picture -->
			<div class="relative">
				{#if data.user?.profile_picture || data.user?.avatar_url}
					<img
						src={data.user?.profile_picture || data.user?.avatar_url}
						alt="Profile_Picture"
						class="w-32 h-32 rounded-full object-cover border-4 border-white shadow-lg"
					/>
				{:else}
					<div
						class="w-32 h-32 rounded-full bg-gradient-to-br from-primary/80 to-secondary/80 flex items-center justify-center border-4 border-white shadow-lg"
					>
						<User size={56} weight="bold" class="text-white" />
					</div>
				{/if}
				<button
					class="absolute bottom-0 right-0 bg-secondary text-white p-2 rounded-full shadow-md hover:bg-secondary/80 transition-colors"
				>
					<PencilSimple size={18} weight="bold" />
				</button>
			</div>

			<!-- User Info Header -->
			<div class="flex flex-col items-center md:items-start">
				<h1 class="text-3xl font-bold text-center md:text-left">
					{data.user?.first_name}
					{data.user?.last_name}
				</h1>
				<p class="text-base text-primary/70 flex items-center gap-1 mt-1">
					<At size={16} weight="bold" />
					{data.user.username}
				</p>
				<p class="text-sm text-primary/60 flex items-center gap-1 mt-2">
					<Calendar size={16} />
					Member since {joinedDate}
				</p>
			</div>
		</div>
	</div>

	<!-- User Information Card -->
	<div class="bg-white rounded-xl shadow-md p-6 border border-base-200">
		<h2 class="text-xl font-bold border-b pb-3 mb-4">User Information</h2>

		<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
			<!-- Personal Information -->
			<div>
				<h3 class="text-lg font-semibold mb-3 text-primary/90">Personal Details</h3>
				<ul class="space-y-4">
					<li class="flex items-center gap-3">
						<div class="bg-primary/10 p-2 rounded-full">
							<User size={20} weight="bold" class="text-primary" />
						</div>
						<div>
							<p class="text-sm text-primary/60">Full Name</p>
							<p class="font-medium">{data.user?.first_name} {data.user?.last_name}</p>
						</div>
					</li>
					<li class="flex items-center gap-3">
						<div class="bg-primary/10 p-2 rounded-full">
							<At size={20} weight="bold" class="text-primary" />
						</div>
						<div>
							<p class="text-sm text-primary/60">Username</p>
							<p class="font-medium">{data.user.username}</p>
						</div>
					</li>
					<li class="flex items-center gap-3">
						<div class="bg-primary/10 p-2 rounded-full">
							<Envelope size={20} weight="bold" class="text-primary" />
						</div>
						<div>
							<p class="text-sm text-primary/60">Email Address</p>
							<p class="font-medium">{data.user.email}</p>
						</div>
					</li>
				</ul>
			</div>

			<div class=" rounded-lg shadow-sm p-4">
				<h3 class="text-lg font-semibold mb-3 text-primary/90">Account Stats</h3>
				<div class="grid grid-cols-2 gap-4">
					<div class="bg-white rounded-lg p-3 shadow-sm">
						<p class="text-sm text-primary/60">Tickets Purchased</p>
						<p class="text-2xl font-bold text-secondary">0</p>
					</div>
					<div class="bg-white rounded-lg p-3 shadow-sm">
						<p class="text-sm text-primary/60">Total Spending</p>
						<p class="text-2xl font-bold text-secondary">
							{data?.totalSpent ? data.totalSpent : 0}
						</p>
					</div>
				</div>
			</div>
		</div>

		<!-- Action Buttons -->
		<div class="flex justify-end mt-6 gap-3">
			<button class="btn btn-outline">Edit Profile</button>
			<button class="btn btn-primary">Change Password</button>
		</div>
	</div>
</div>
