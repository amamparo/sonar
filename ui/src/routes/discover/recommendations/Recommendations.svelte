<script>
	import Tile from '../Tile.svelte';
	import { trackStore, api } from '$lib';

	let recommendations = [];
	trackStore.subscribe(state => {
		recommendations = api.getRecommendations(state.tracks);
	});
</script>

<Tile class="w-2/3">
	<svelte:fragment slot="header">
		Recommendations
	</svelte:fragment>
	<div class="h-full flex items-center justify-center pb-20 text-muted">
		Recommendations will be available after you've added tracks to your playlist.
	</div>
</Tile>