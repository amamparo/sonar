<script>
	import { ContextMenu, trackStore } from '$lib';
	import AddSongsIcon from './icon/AddSongsIcon.svelte';
	import ExportIcon from './icon/ExportIcon.svelte';
	import TrashIcon from '$lib/components/icon/Trash.svelte';
	import ImportIcon from './icon/ImportIcon.svelte';
	import ImportPlaylistSubMenu from './ImportPlaylistSubMenu.svelte';
	import AddSongsSubMenu from './addSongsSubMenu/AddSongsSubMenu.svelte';
	import ConfirmClearModal from './ConfirmClearModal.svelte';

	export let subMenuToShow = null;

	let hasTracks = false;
	trackStore.subscribe(({ tracks }) => {
		hasTracks = tracks && tracks.length > 0;
	});

	let isConfirmingClear = false;
	const confirmClear = () => {
		isConfirmingClear = true;
	};
</script>

<ContextMenu bind:subMenuToShow={subMenuToShow} menuClass={'w-44 z-20'} items={[
		{
			icon: AddSongsIcon,
			text: 'Add Tracks',
			subMenu: AddSongsSubMenu
		},
		{
			icon: ImportIcon,
			text: 'Import Playlist',
			subMenu: ImportPlaylistSubMenu
		},
		{
			icon: ExportIcon,
			text: 'Export Playlist',
			isDisabled: true,
			action: () => console.log('Exporting playlist')
		},
		{
			icon: TrashIcon,
			text: 'Clear',
			isDisabled: !hasTracks,
			action: () => {
				confirmClear()
			}
		}
	]} />

{#if isConfirmingClear}
	<ConfirmClearModal on:close={() => isConfirmingClear = false}/>
{/if}