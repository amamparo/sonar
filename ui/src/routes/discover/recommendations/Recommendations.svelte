<script lang="ts">
	import { api, type Recommendations, trackStore } from '$lib';
	import Button from '$lib/components/Button.svelte';
	import Spinner from '$lib/components/icon/Spinner.svelte';
	import Tile from '../Tile.svelte';
	import Chart from './Chart.svelte';

	let isLoading = true;
	let recommendations: Recommendations | null = null;
	trackStore.subscribe(async (state) => {
		if (state.tracks.length === 0) {
			recommendations = null;
			return;
		}
		isLoading = true;
		recommendations = await api.getRecommendations(state.tracks);
		isLoading = false;
	});

	let selectedTracks = [];

	function addSelectedTracksToPlaylist() {
		trackStore.addAll(selectedTracks);
		selectedTracks = [];
		clearSelections();
	}

	const setSelectedTracks = (tracks) => {
		selectedTracks = tracks;
	};

	let clearSelections
</script>

<Tile class="w-2/3">
	<svelte:fragment slot="header">
		Recommendations
	</svelte:fragment>
	{#if isLoading}
		<div class="h-full flex items-center justify-center">
			<Spinner />
		</div>
	{:else if !recommendations || recommendations.recommendations.length === 0}
		<div class="h-full flex items-center justify-center text-muted">
			Recommendations will be available after you've added tracks to your playlist.
		</div>
	{:else}
		<div class="flex flex-col h-full">
			<div class="flex-grow">
				<div class="h-full w-full overflow-hidden">
					<Chart bind:recommendations={recommendations} bind:clearSelections={clearSelections} setSelectedTracks={setSelectedTracks} />
				</div>
			</div>
			<div class="items-center justify-center mx-auto p-4">
				{#if selectedTracks && selectedTracks.length > 0}
					<Button onClick={addSelectedTracksToPlaylist}>
						Add {selectedTracks.length} Track{selectedTracks.length > 1 ? 's' : ''}
					</Button>
				{:else}
					<span class="text-muted font-circular-book">Click on recommendations to queue them for your playlist.</span>
				{/if}
			</div>
		</div>
	{/if}
</Tile>