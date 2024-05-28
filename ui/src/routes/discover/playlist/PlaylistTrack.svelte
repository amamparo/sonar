<script>
	import { previewPlayer, trackStore } from '$lib';
	import TrashIcon from '$lib/components/icon/Trash.svelte';
	import Play from '$lib/components/icon/Play.svelte';
	import Stop from '$lib/components/icon/Stop.svelte';

	export let imageUrl;
	export let album;
	export let title;
	export let artist;
	export let id;
	export let previewUrl;

	let isHovered = false;

	const hover = newIsHovered => () => {
		isHovered = newIsHovered;
	};

	const deleteTrack = () => {
		trackStore.delete(id);
	};

	let isPreviewPlaying = false;
	let previewDuration = 0;
	previewPlayer.subscribe(state => {
		isPreviewPlaying = state.currentSource === id;
		previewDuration = state.currentDuration;
	});
</script>


<div class="flex items-center p-2.5 hover:bg-foreground rounded" on:pointerenter={hover(true)}
		 on:pointerleave={hover(false)}>
	<div class="relative w-12 h-12 flex-none rounded overflow-hidden hover:cursor-pointer">
		<img src={imageUrl} alt={album} class="absolute" />
		{#if isHovered || isPreviewPlaying}
			<div class="relative h-full w-full rounded absolute z-20"
					 on:click={() => previewPlayer.toggle(previewUrl, id)}>
				<div class="absolute bg-background inset-0 z-30 opacity-70"></div>
				{#if isPreviewPlaying && previewDuration}
					<div class="absolute preview-progress bg-spotify-green inset-0 z-40 opacity-50"
							 style="animation-duration: {previewDuration}s;"></div>
				{/if}
				<div class="absolute inset-0 p-3 hover:p-2.5 hover:transition-all transition-all fill-primary z-50">
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
		<div class="text-base text-primary truncate">{title}</div>
		<div class="text-sm text-secondary truncate">{artist}</div>
	</div>
	{#if isHovered}
		<div class="w-10 h-10 p-3 fill-muted hover:fill-red-600 hover:cursor-pointer"
				 on:click={deleteTrack}>
			<TrashIcon />
		</div>
	{/if}
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