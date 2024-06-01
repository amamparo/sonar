<script lang="ts">
	import { onDestroy, onMount } from 'svelte';

	import MagnifyingGlass from '../icon/MagnifyingGlass.svelte';

	import _ from 'lodash';
	import { api, type Track, trackStore } from '$lib';
	import AddSongsSearchResult from './AddSongsSearchResult.svelte';

	let searchQuery = '';
	let searchResults: Track[] = [];
	let scrollable = null;

	let searchInput = null;

	let tracks = [];
	trackStore.subscribe(state => {
		tracks = state.tracks;
	});

	const isAdded = id => {
		return tracks.some(track => track.id === id);
	};

	export let onComplete = () => {
	};

	const debouncedHandler = _.debounce(async (query) => {
		const trimmed = query.trim().toLowerCase();
		if (!trimmed) {
			searchResults = [];
			return;
		}
		searchResults = await api.searchTracks(trimmed);
		if (scrollable) {
			scrollable.scrollTop = 0;
		}
	}, 500);

	function handleInput(event) {
		searchQuery = event.target.value;
		debouncedHandler(searchQuery);
	}

	onDestroy(() => {
		debouncedHandler.cancel();
	});

	onMount(() => {
		searchInput.focus();
	});
</script>

<div class="p-1 w-96">
	<div class="relative">
		<div class="absolute inset-y-0 start-0 flex items-center ps-3 pointer-events-none">
			<MagnifyingGlass />
		</div>
		<input class="bg-highlight block w-full p-2 ps-10 text-sm rounded focus:outline-none"
					 placeholder="Search by title, artist, or album" on:input={handleInput} bind:this={searchInput} />
	</div>
	{#if searchResults.length}
		<div class="results mt-2 max-h-[75vh] overflow-y-auto overflow-x-hidden" bind:this={scrollable}>
			{#each searchResults as track}
				<AddSongsSearchResult {track}/>
			{/each}
		</div>
	{/if}
</div>