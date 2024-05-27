<script>
	import { ContextMenu, trackStore } from '$lib';
	import AddSongsIcon from './icon/AddSongsIcon.svelte';
	import ExportIcon from './icon/ExportIcon.svelte';
	import TrashIcon from './icon/TrashIcon.svelte';
	import ImportIcon from './icon/ImportIcon.svelte';
	import ImportPlaylistSubMenu from './ImportPlaylistSubMenu.svelte';

	export let subMenuToShow = null
</script>

<ContextMenu bind:subMenuToShow={subMenuToShow} menuClass={'w-44'} items={[
		{
			icon: AddSongsIcon,
			text: 'Add Songs'
		},
		{
			icon: ImportIcon,
			text: 'Import Playlist',
			subMenu: ImportPlaylistSubMenu
		},
		{
			icon: ExportIcon,
			text: 'Export Playlist',
			action: () => console.log('Exporting playlist')
		},
		{
			icon: TrashIcon,
			text: 'Clear',
			action: () => {
				trackStore.clear();
			}
		}
	]}/>