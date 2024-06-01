<script lang="ts">
	import { api, type Track, trackStore } from '$lib';
	import Button from '$lib/components/Button.svelte';
	import Spinner from '$lib/components/icon/Spinner.svelte';
	import Tile from '../Tile.svelte';
	import Chart from './Chart.svelte';
	import selectedTrackStore from './selectedTrackStore';
	import _ from 'lodash'

	let isLoading = true;
	let recommendations: Track[] | null = null;

	let abortController;

	const fetchRecommendations = _.debounce(async (tracks) => {
		if (abortController) {
			abortController.abort();
		}
		if (tracks.length === 0) {
			recommendations = null;
			isLoading = false;
			return;
		}
		abortController = new AbortController();
		isLoading = true;
		recommendations = await api.getRecommendations(tracks, abortController.signal)
		isLoading = false;
	}, 300);

	trackStore.subscribe(async ({tracks}) => await fetchRecommendations(tracks));

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
		<div class="flex h-full flex-grow justify-content items-center mx-auto">
			<Spinner />
		</div>
	{:else if recommendations === null}
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
					<Button onClick={addSelections} class="hover:border-spotify-green hover:text-spotify-green">
						Add {selectedTracks.length} Track{selectedTracks.length > 1 ? 's' : ''}
					</Button>
					<Button onClick={selectedTrackStore.clear} class="hover:border-red-600 hover:text-red-600">
						Clear Selections
					</Button>
				{:else}
					<span class="text-muted font-circular-book">Click on recommendations to queue them for your playlist.</span>
				{/if}
			</div>
		</div>
	{/if}
</Tile>