<script>
	import { onDestroy } from 'svelte';

	import MagnifyingGlass from './icon/MagnifyingGlass.svelte';

	import _ from 'lodash';
	import { api } from '$lib';

	let searchQuery = '';
	let searchResults = [];
	let scrollable = null;
	export let onComplete = () => {
	};

	const debouncedHandler = _.debounce(async (query) => {
		const trimmed = query.trim().toLowerCase();
		if (!trimmed) {
			searchResults = [];
			return;
		}
		searchResults = await api.get(`/search/playlists/${trimmed}`);
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

	const onClick = (id) => {
		console.log(id);
		onComplete();
	};
</script>

<div class="p-1 w-96">
	<div class="relative">
		<div class="absolute inset-y-0 start-0 flex items-center ps-3 pointer-events-none">
			<MagnifyingGlass />
		</div>
		<input class="bg-highlight block w-full p-2 ps-10 text-sm rounded focus:outline-none"
					 placeholder="Search for a playlist" on:input={handleInput} />
	</div>
	{#if searchResults.length}
		<div class="results mt-2 max-h-[75vh] overflow-y-auto overflow-x-hidden" bind:this={scrollable}>
			{#each searchResults as { author, id, image, name }}
				<div class="flex items-center p-2 px-2.5 rounded hover:bg-highlight hover:cursor-pointer"
						 on:click={onClick(id)}>
					<img class="w-12 h-12 rounded" src={image} alt={name} />
					<div class="flex flex-col ms-3 overflow-hidden">
						<div class="text-base text-primary truncate">{name}</div>
						<div class="text-sm text-secondary truncate">{author}</div>
					</div>
				</div>
			{/each}
		</div>
	{/if}
</div>