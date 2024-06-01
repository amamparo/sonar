<script>
	import { previewPlayer, trackStore } from '$lib';
	import TrashIcon from '$lib/components/icon/Trash.svelte';
	import PreviewableTrackDetails from '$lib/components/PreviewableTrackDetails.svelte';

	export let track;

	let isHovered = false;

	let isPreviewPlaying = false;

	const hover = newIsHovered => () => {
		isHovered = newIsHovered;
	};

	const deleteTrack = () => {
		trackStore.delete(track.id);
		if (isPreviewPlaying) {
			previewPlayer.stop();
		}
	};
</script>


<div class="flex items-center p-2.5 hover:bg-foreground rounded" on:pointerenter={hover(true)}
		 on:pointerleave={hover(false)}>
	<PreviewableTrackDetails {track} shouldShowPlay={isHovered} sourcePrefix="playlist"
													 bind:isPreviewPlaying={isPreviewPlaying}/>
	{#if isHovered}
		<div class="w-10 h-10 p-3 fill-muted hover:fill-red-600 hover:cursor-pointer"
				 on:click={deleteTrack}>
			<TrashIcon />
		</div>
	{/if}
</div>