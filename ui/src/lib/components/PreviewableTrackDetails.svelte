<script>
	import { previewPlayer } from '$lib';
	import Play from '$lib/components/icon/Play.svelte';
	import Stop from '$lib/components/icon/Stop.svelte';
	import { onDestroy } from 'svelte';

	export let sourcePrefix = '';
	export let track;
	export let shouldShowPlay = false;
	export let isPreviewPlaying = false;

	$: sourceKey = `${sourcePrefix}-${track.id}`;

	let currentlyPlayingSourceKey = null;
	let previewDuration = 0;
	previewPlayer.subscribe(state => {
		currentlyPlayingSourceKey = state.currentSourceKey;
		previewDuration = state.currentDuration;
	});

	$: isPreviewPlaying = currentlyPlayingSourceKey && currentlyPlayingSourceKey === sourceKey;

	onDestroy(() => {
		if (isPreviewPlaying) {
			previewPlayer.stop();
		}
	})
</script>

<div class="relative w-12 h-12 flex-none rounded overflow-hidden {track.previewUrl ? 'hover:cursor-pointer' : ''}">
	<img src={track.imageUrl} class="absolute" />
	{#if track.previewUrl && (shouldShowPlay || isPreviewPlaying)}
		<div class="relative h-full w-full rounded absolute z-20"
				 on:click={() => previewPlayer.toggle(track, sourceKey)}>
			<div class="absolute bg-background inset-0 z-30 opacity-70"></div>
			{#if isPreviewPlaying && previewDuration}
				<div class="absolute preview-progress bg-spotify-green inset-0 z-40 opacity-50"
						 style="animation-duration: {previewDuration}s;"></div>
			{/if}
			<div class="absolute inset-0 p-3.5 hover:p-3 hover:transition-all transition-all fill-primary z-50">
				{#if isPreviewPlaying}
					<Stop />
				{:else}
					<Play />
				{/if}
			</div>
		</div>
	{/if}
</div>
<div class="flex flex-col flex-1 ms-3 overflow-hidden">
	<div class="text-base truncate {isPreviewPlaying ? 'text-spotify-green'  : 'text-primary'}">
		{track.title}
	</div>
	<div class="text-sm text-secondary truncate">{track.artists.map(x => x.name).join(", ")}</div>
</div>

<style>
    @keyframes preview-progress {
        0% {
            transform: translateX(-100%);
        }
        100% {
            transform: translateX(0);
        }
    }

    .preview-progress {
        animation: preview-progress linear forwards;
    }
</style>