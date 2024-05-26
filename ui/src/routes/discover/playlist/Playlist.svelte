<script>
	import AddSongsModal from './AddSongsModal.svelte';
	import Tile from '../Tile.svelte';
	import PlaylistContextMenu from './contextMenu/PlaylistContextMenu.svelte';

	let addingSong = false;
</script>

<Tile class="w-1/3">
	<svelte:fragment slot="header">
		<div>Playlist</div>
		<PlaylistContextMenu />
	</svelte:fragment>
</Tile>
{#if addingSong}
	<AddSongsModal />
{/if}