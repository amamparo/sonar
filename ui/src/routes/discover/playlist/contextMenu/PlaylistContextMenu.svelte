<script>
	import { ContextMenu } from '$lib';
	import AddSongsIcon from './icon/AddSongsIcon.svelte';
	import ExportIcon from './icon/ExportIcon.svelte';
	import TrashIcon from './icon/TrashIcon.svelte';
	import ImportIcon from './icon/ImportIcon.svelte';
</script>

<ContextMenu items={[
		{ icon: AddSongsIcon, text: 'Add Songs', action: () => alert('Adding song') },
		{ icon: ImportIcon, text: 'Import Playlist', action: () => alert('Importing playlist') },
		{ icon: ExportIcon, text: 'Export Playlist', action: () => alert('Exporting playlist') },
		{ icon: TrashIcon, text: 'Clear', action: () => alert('Clearing playlist') }
	]} menuClass={'w-44'}/>

<style lang="scss">
</style>