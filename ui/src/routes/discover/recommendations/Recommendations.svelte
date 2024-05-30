<script lang="ts">
	import { api, type Recommendations, trackStore } from '$lib';
	import Button from '$lib/components/Button.svelte';
	import Spinner from '$lib/components/icon/Spinner.svelte';
	import Tile from '../Tile.svelte';
	import Chart from './Chart.svelte';
	import selectedTrackStore from './selectedTrackStore';

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
	selectedTrackStore.subscribe(tracks => {
		selectedTracks = tracks;
	});

	const addSelections = () => {
		trackStore.addAll(selectedTracks);
		selectedTrackStore.clear();
	};
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
			<div class="w-full flex-grow">
				<Chart {recommendations} />
			</div>
			<div class="items-center justify-center mx-auto p-3 pb-5 space-x-2">
				{#if selectedTracks && selectedTracks.length > 0}
					<Button onClick={selectedTrackStore.clear} class="hover:border-red-600 hover:text-red-600">
						Clear Selections
					</Button>
					<Button onClick={addSelections} class="hover:border-spotify-green hover:text-spotify-green">
						Add {selectedTracks.length} Track{selectedTracks.length > 1 ? 's' : ''}
					</Button>
				{:else}
					<span class="text-muted font-circular-book">Click on recommendations to queue them for your playlist.</span>
				{/if}
			</div>
		</div>
	{/if}
</Tile>