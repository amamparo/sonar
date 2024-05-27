<script>
	import { trackStore } from '$lib';
	import TrashIcon from '$lib/components/icon/Trash.svelte';

	export let imageUrl;
	export let album;
	export let title;
	export let artist;
	export let id;

	let isHovered = false;

	const hover = newIsHovered => () => {
		isHovered = newIsHovered;
	};

	const deleteTrack = () => {
		trackStore.delete(id);
	}
</script>


<div class="flex items-center p-2.5 hover:bg-foreground rounded" on:pointerenter={hover(true)}
		 on:pointerleave={hover(false)}>
	<div class="w-12 h-12 flex-none rounded overflow-hidden">
		<img src={imageUrl} alt={album} />
	</div>
	<div class="flex flex-col flex-1 ms-3 overflow-hidden">
		<div class="text-base text-primary font-extralight truncate">{title}</div>
		<div class="text-sm text-secondary truncate">{artist}</div>
	</div>
	{#if isHovered}
		<div class="w-10 h-10 p-3 fill-muted hover:fill-red-600 hover:cursor-pointer"
				 on:click={deleteTrack}>
			<TrashIcon />
		</div>
	{/if}
</div>