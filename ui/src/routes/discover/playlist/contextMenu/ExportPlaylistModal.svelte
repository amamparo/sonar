<script>
	import { createEventDispatcher, onMount } from 'svelte';
	import Button from '$lib/components/Button.svelte';
	import { api, trackStore } from '$lib';
	import Modal from '$lib/components/Modal.svelte';

	let playlistName;

	let playlistNameInput;

	let tracks;

	trackStore.subscribe(state => {
		tracks = state.tracks;
	});

	$: disableConfirm = !playlistName;

	const dispatch = createEventDispatcher();

	const close = () => dispatch('close');

	const confirm = async () => {
		await api.exportPlaylist(playlistName, tracks.map(t => t.id));
		close();
	};

	onMount(() => {
		if (playlistNameInput) {
			playlistNameInput.focus();
		}
	});

	$: confirmButtonClass = disableConfirm ?
		'border-muted text-muted hover:cursor-default' :
		'border-secondary text-secondary hover:border-spotify-green hover:text-spotify-green';
</script>

<Modal on:close={close}>
	<input class="bg-highlight block w-full p-2 text-sm rounded focus:outline-none w-full"
				 placeholder="Name your new playlist" bind:value={playlistName}
				 bind:this={playlistNameInput}/>
	<div class="flex w-full mt-4 justify-end space-x-3">
		<Button class="border-secondary text-secondary hover:border-red-600 hover:text-red-600"
						on:click={close}>
			Cancel
		</Button>
		<Button on:click={!disableConfirm && confirm} disabled={disableConfirm}
						class={confirmButtonClass}>
			Export
		</Button>
	</div>
</Modal>
