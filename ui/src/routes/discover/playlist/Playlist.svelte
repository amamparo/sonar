<script>
	import Button from '$lib/components/Button.svelte';
	import AddSongsModal from './AddSongsModal.svelte';

	let addingSong = false

	function addSong() {
		addingSong = true
	}
</script>

<div class="flex justify-between items-center font-circular-bold text-lg pb-3">
	<div>Your Playlist</div>
	<Button text="Add" onClick={addSong}/>
</div>
{#if addingSong}
	<AddSongsModal/>
{/if}