<script lang="ts">
	import { goto } from '$app/navigation';
	import { MagnifyingGlass } from 'phosphor-svelte';

	// รับค่า default searchQuery จาก props (ถ้ามี)
	let { defaultQuery = '', customClass = '' } = $props();

	// สร้าง state สำหรับเก็บค่า search
	let searchQuery = $state(defaultQuery);

	// ฟังก์ชันจัดการการค้นหา
	function handleSearch() {
		// กรณีมี query ให้ไปที่หน้า events พร้อมกับ query parameter
		if (searchQuery) {
			goto(`/events?search=${encodeURIComponent(searchQuery)}`, {
				keepFocus: true,
				invalidateAll: true
			});
		} else {
			// กรณีไม่มี query ให้ไปที่หน้า events โดยไม่มี parameter
			goto('/events', { keepFocus: true, invalidateAll: true });
		}
	}
</script>

<!-- UI ส่วนของ search bar -->
<form
	class="card bg-base-100 shadow-xl flex flex-row justify-center w-full h-[50px] {customClass}"
	onsubmit={(e) => {
		e.preventDefault();
		handleSearch();
	}}
>
	<input
		type="text"
		placeholder="Search events"
		class="input input-bordered w-full h-full bg-none rounded-l-lg rounded-r-none focus:outline-none focus:border-transparent focus:ring-0 border-0"
		bind:value={searchQuery}
		onkeydown={(e) => e.key === 'Enter' && handleSearch()}
	/>
	<button
		class="flex items-center justify-center bg-secondary border-0 rounded-l-none rounded-r-lg h-full w-[60px] hover:bg-blend-saturation cursor-pointer transition-colors duration-50"
		type="submit"
		aria-label="Search"
		title="Search"
	>
		<MagnifyingGlass size={24} class="text-secondary-content" weight="bold" />
	</button>
</form>
