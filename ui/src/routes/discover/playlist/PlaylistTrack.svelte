<script>
	import { previewPlayer, trackStore } from '$lib';
	import TrashIcon from '$lib/components/icon/Trash.svelte';
	import Play from '$lib/components/icon/Play.svelte';
	import { onMount } from 'svelte';

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

	let isPreviewPlaying = false
	previewPlayer.subscribe(state => {
		isPreviewPlaying = state.currentSource === id
	})
</script>


<div class="flex items-center p-2.5 hover:bg-foreground rounded" on:pointerenter={hover(true)}
		 on:pointerleave={hover(false)}>
	<div class="relative w-12 h-12 flex-none rounded overflow-hidden hover:cursor-pointer">
		<img src={imageUrl} alt={album} class="absolute" />
		{#if isHovered || isPreviewPlaying}
			<div class="bg-background h-full w-full rounded absolute z-50 opacity-70" on:click={() => previewPlayer.toggle(previewUrl, id)}>
				<div class="fill-primary p-3 hover:p-2.5 hover:transition-all transition-all">
					<Play />
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