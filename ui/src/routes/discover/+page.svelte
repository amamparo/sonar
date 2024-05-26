<script lang="ts">
	import { onMount } from 'svelte';
	import { api } from '$lib';
	import Tile from './Tile.svelte';
	import Playlist from './playlist/Playlist.svelte';

	onMount(() => {
		if (!api.hasToken()) {
			window.location.href = '/auth';
		}
	});
</script>

<div class="flex min-h-screen p-3 space-x-3">
	<Playlist />
	<Tile class="w-2/3">
		<svelte:fragment slot="header">
			Analysis
		</svelte:fragment>
	</Tile>
</div>