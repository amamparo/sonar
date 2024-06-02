<script>
	import Tile from '../Tile.svelte';
	import PlaylistContextMenu from './contextMenu/PlaylistContextMenu.svelte';
	import { trackStore } from '$lib';
	import Spinner from '$lib/components/icon/Spinner.svelte';
	import Button from '$lib/components/Button.svelte';
	import ImportPlaylistSubMenu from './contextMenu/ImportPlaylistSubMenu.svelte';
	import PlaylistTrack from './PlaylistTrack.svelte';
	import AddSongsSubMenu from './contextMenu/addSongsSubMenu/AddSongsSubMenu.svelte';

	let tracks = [];
	let isUpdating = false;
	trackStore.subscribe(x => {
		tracks = x.tracks;
		isUpdating = x.isUpdating;
	});

	let subMenuToShow = null;

	const show = subMenu => () => {
		subMenuToShow = subMenu;
	};
</script>

<Tile class="flex flex-col w-1/3">
	<svelte:fragment slot="header">
		<div>
			Playlist
			<span class="text-muted font-circular-medium font-extralight">
				{
					tracks.length && !isUpdating ?
						` (${tracks.length} track${tracks.length > 1 ? 's' : ''})` :
						""
				}
			</span>
		</div>
		<PlaylistContextMenu bind:subMenuToShow={subMenuToShow} />
	</svelte:fragment>
	<div class="flex-grow overflow-auto">
		{#if isUpdating}
			<div class="h-full flex items-center justify-center">
				<Spinner />
			</div>
		{:else if tracks.length === 0}
			<div class="h-full flex items-center justify-center pb-20">
				<Button onClick={show(AddSongsSubMenu)}>Add Tracks</Button>
				<span class="px-2">or</span>
				<Button onClick={show(ImportPlaylistSubMenu)}>Import Playlist</Button>
			</div>
		{:else}
			{#each tracks as track}
				<PlaylistTrack {track} />
			{/each}
		{/if}
	</div>
</Tile>