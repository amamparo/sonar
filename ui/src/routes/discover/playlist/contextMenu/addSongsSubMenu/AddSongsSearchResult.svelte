<script lang="ts">
	import { type Track, trackStore } from '$lib';
	import Check from '$lib/components/icon/Check.svelte';
	import Plus from '$lib/components/icon/Plus.svelte';
	import Trash from '$lib/components/icon/Trash.svelte';
	import PreviewableTrackDetails from '$lib/components/PreviewableTrackDetails.svelte';

	export let track: Track;

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

	$: isAdded = tracks.some(t => t.id === track.id);

	const onIconClick = () => {
		if (isAdded) {
			trackStore.delete(track.id);
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
</script>

<div class="flex items-center p-2.5 pr-0 rounded hover:bg-highlight"
		 on:pointerenter={hover(true)} on:pointerleave={hover(false)}>
	<PreviewableTrackDetails {track} shouldShowPlay={isHovered} sourcePrefix="track-search"/>
	{#if icon}
		<div class="w-10 h-10 p-3 hover:cursor-pointer {iconFillClass}"
				 on:click={onIconClick} on:pointerenter={hoverIcon(true)}
				 on:pointerleave={hoverIcon(false)}>
			<svelte:component this={icon} />
		</div>
	{/if}
</div>