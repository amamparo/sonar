<script lang="ts">
	import { api, type Track, trackStore } from '$lib';
	import Spinner from '$lib/components/icon/Spinner.svelte';
	import Tile from '../Tile.svelte';
	import Chart from './Chart.svelte';
	import _ from 'lodash';

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
		recommendations = await api.getRecommendations(tracks.map(t => t.id), abortController.signal);
		isLoading = false;
	}, 300);

	trackStore.subscribe(async ({ tracks }) => await fetchRecommendations(tracks));
</script>

<Tile class="w-2/3 2xl:w-3/4 px-0">
	<div slot="header" class="px-2">
		Recommendations
	</div>
	{#if isLoading}
		<div class="flex h-full flex-grow justify-content items-center mx-auto">
			<Spinner />
		</div>
	{:else if recommendations === null}
		<div class="h-full flex items-center justify-center text-muted">
			Recommendations will be available after you've added tracks to your playlist.
		</div>
	{:else}
		<Chart {recommendations} />
	{/if}
</Tile>