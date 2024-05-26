<script lang="ts">
	import { onMount } from 'svelte';
	import { api } from '$lib';
	import Tile from './Tile.svelte';

	onMount(() => {
		if (!api.hasToken()) {
			window.location.href = '/auth';
		}
	});
</script>

<div class="flex min-h-screen p-3 space-x-3">
	<Tile class="w-1/3" title="Your Playlist">
		<p>This is the left column, occupying 25% of the screen width.</p>
	</Tile>
	<Tile class="w-2/3">
		<h2 class="text-xl font-bold mb-4">Right Column</h2>
		<p>This is the right column, occupying the remaining 75% of the screen width.</p>
	</Tile>
</div>