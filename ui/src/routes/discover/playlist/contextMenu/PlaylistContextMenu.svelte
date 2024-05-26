<script>
	import { ContextMenu } from '$lib';
	import AddSongsIcon from './icon/AddSongsIcon.svelte';
	import ExportIcon from './icon/ExportIcon.svelte';
	import TrashIcon from './icon/TrashIcon.svelte';
	import ImportIcon from './icon/ImportIcon.svelte';
	import ImportPlaylistSubMenu from './ImportPlaylistSubMenu.svelte';
</script>

<ContextMenu menuClass={'w-44'} items={[
		{
			icon: AddSongsIcon,
			text: 'Add Songs',
			subMenu: ImportPlaylistSubMenu
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
			action: () => console.log('Clearing playlist')
		}
	]}/>