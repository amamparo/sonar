<script>
	import { previewPlayer, trackStore } from '$lib';
	import TrashIcon from '$lib/components/icon/Trash.svelte';
	import PlayableTrackArt from '$lib/components/PlayableTrackArt.svelte';

	export let track;

	let isHovered = false;

	const hover = newIsHovered => () => {
		isHovered = newIsHovered;
	};

	const deleteTrack = () => {
		trackStore.delete(track.id);
	};

	let isPreviewPlaying = false;
	let previewDuration = 0;
	previewPlayer.subscribe(state => {
		isPreviewPlaying = state.currentSource === track.id;
		previewDuration = state.currentDuration;
	});
</script>


<div class="flex items-center p-2.5 hover:bg-foreground rounded" on:pointerenter={hover(true)}
		 on:pointerleave={hover(false)}>
	<PlayableTrackArt {track} shouldShowPlay={isHovered} />
	<div class="flex flex-col flex-1 ms-3 overflow-hidden">
		<div class="text-base text-primary truncate">{track.title}</div>
		<div class="text-sm text-secondary truncate">{track.artist}</div>
	</div>
	{#if isHovered}
		<div class="w-10 h-10 p-3 fill-muted hover:fill-red-600 hover:cursor-pointer"
				 on:click={deleteTrack}>
			<TrashIcon />
		</div>
	{/if}
</div>