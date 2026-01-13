<script>
	const Features = [
		{
			title: 'Event Management',
			description: 'Manage your events with ease.',
			link: ''
		},
		{
			title: 'Staff Organization',
			link: ''
		},
		{
			title: 'Analytics',
			link: ''
		},
		{
			title: 'Ticketing',
			link: ''
		}
	];

	const Resources = [
		{
			title: 'Documentation',
			link: '/docs'
		},
		{
			title: 'API',
			link: '/api'
		},
		{
			title: 'Blog',
			link: '/blog'
		},
		{
			title: 'Support',
			link: '/support'
		}
	];

	const Company = [
		{
			title: 'About Us',
			link: '/about'
		},
		{
			title: 'Careers',
			link: '/careers'
		},
		{
			title: 'Contact',
			link: '/contact'
		},
		{
			title: 'Terms & Privacy',
			link: '/terms'
		}
	];
</script>

<footer class="bg-neutral text-neutral-content">
	<div class="container mx-auto px-6 py-10">
		<div class="grid grid-cols-2 md:grid-cols-4 gap-8">
			<div>
				<h3 class="text-lg font-bold mb-4">EventSquare</h3>
				<p class="text-sm opacity-75">
					Empowering event organizers with powerful tools since 2025.
				</p>
			</div>

			<div>
				<h3 class="text-lg font-bold mb-4">Features</h3>
				<ul class="space-y-2 text-sm opacity-75">
					{#each Features as { title, link }}
						<li>
							<a href={link} class="hover:underline">{title}</a>
						</li>
					{/each}
				</ul>
			</div>

			<div>
				<h3 class="text-lg font-bold mb-4">Resources</h3>
				<ul class="space-y-2 text-sm opacity-75">
					{#each Resources as { title, link }}
						<li>
							<a href={link} class="hover:underline">{title}</a>
						</li>
					{/each}
				</ul>
			</div>

			<div>
				<h3 class="text-lg font-bold mb-4">Company</h3>
				<ul class="space-y-2 text-sm opacity-75">
					{#each Company as { title, link }}
						<li>
							<a href={link} class="hover:underline">{title}</a>
						</li>
					{/each}
				</ul>
			</div>
		</div>

		<div
			class="border-t border-neutral-content/20 mt-10 pt-6 flex flex-col md:flex-row justify-between items-center"
		>
			<p class="text-sm opacity-75">© 2025 EventSquare. All rights reserved.</p>
			<div class="flex gap-4 mt-4 md:mt-0">
				<a href="#" class="opacity-75 hover:opacity-100">Twitter</a>
				<a href="#" class="opacity-75 hover:opacity-100">LinkedIn</a>
				<a href="#" class="opacity-75 hover:opacity-100">Facebook</a>
				<a href="#" class="opacity-75 hover:opacity-100">Instagram</a>
			</div>
		</div>
	</div>
</footer>
