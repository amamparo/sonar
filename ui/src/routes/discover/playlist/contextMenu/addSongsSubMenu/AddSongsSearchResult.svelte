<script lang="ts">
	import { type Track, trackStore } from '$lib';
	import Check from '$lib/components/icon/Check.svelte';
	import Plus from '$lib/components/icon/Plus.svelte';
	import Trash from '$lib/components/icon/Trash.svelte';

	export let track: Track;
	const {id, imageUrl, title, artist} = track;

	let isHovered = false;
	let isIconHovered = false;
	const hover = hovered => () => {
		isHovered = hovered;
	};
	const hoverIcon = hovered => () => {
		isIconHovered = hovered;
	};

	let tracks = [];
	trackStore.subscribe(state => {
		tracks = state.tracks;
	});

	$: isAdded = tracks.some(track => track.id === id);

	const onIconClick = () => {
		if (isAdded) {
			trackStore.delete(id);
		} else {
			trackStore.add(track);
		}
	};

	let icon = null;
	let iconFillClass = ''
	$: {
		if (isAdded) {
			icon = isIconHovered ? Trash : Check;
			iconFillClass = isIconHovered ? 'fill-red-600' : 'fill-spotify-green';
		} else if (isHovered) {
			icon = Plus;
			iconFillClass = isIconHovered ? 'fill-primary' : 'fill-secondary';
		} else {
			icon = null;
		}
	}

	const onClick = async (id) => {
		// onComplete();
		// trackStore.setUpdating(true);
		// const playlistTracks = await api.playlistTracks(id);
		// trackStore.setAll(playlistTracks);
	};
</script>

<div class="flex items-center p-1.5 rounded hover:bg-highlight"
		 on:click={onClick(id)} on:pointerenter={hover(true)} on:pointerleave={hover(false)}>
	<img class="w-12 h-12 flex-none rounded" src={imageUrl} alt={title} />
	<div class="flex flex-col flex-1 ms-2 overflow-hidden">
		<div class="text-base text-primary truncate">{title}</div>
		<div class="text-sm text-secondary truncate">{artist}</div>
	</div>
	{#if icon}
		<div class="w-10 h-10 p-3 hover:cursor-pointer {iconFillClass}"
				 on:click={onIconClick} on:pointerenter={hoverIcon(true)}
				 on:pointerleave={hoverIcon(false)}>
			<svelte:component this={icon} />
		</div>
	{/if}
</div>