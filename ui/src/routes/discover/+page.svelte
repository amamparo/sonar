<script lang="ts">
	import { onMount } from 'svelte';
	import { api } from '$lib';
	import Tile from './Tile.svelte';
	import Playlist from './playlist/Playlist.svelte';
	import { goto } from '$app/navigation';
	import Logout from '$lib/components/icon/Logout.svelte';

	onMount(() => {
		if (!api.hasToken()) {
			window.location.href = '/login';
		}
	});
</script>
<div class="flex flex-col h-screen space-y-3 p-3">
	<div class="w-full bg-midground text-primary p-2 flex justify-between items-center rounded">
		<div class="text-lg pl-4 font-circular-bold">
			Discoverify
		</div>
		<button class="w-8 h-8 p-2 fill-secondary hover:fill-red-600" on:click={() => goto('/logout')}>
			<Logout />
		</button>
	</div>
	<div class="flex-grow overflow-hidden flex">
		<div class="space-x-3 w-full flex">
			<Playlist />
			<Tile class="w-2/3">
				<svelte:fragment slot="header">
					Analysis
				</svelte:fragment>
			</Tile>
		</div>
	</div>
	<footer class="mx-auto text-muted font-circular-book text-sm">
		Copyright &copy; {new Date().getFullYear()} Discoverify
		&nbsp;|&nbsp;
		Created by <a href="https://aaronmamparo.com" target="_blank">Aaron Mamparo</a>
		&nbsp;|&nbsp;
		<a href="mailto:aaronmamparo@gmail.com">Feedback?</a>
	</footer>
</div>

<style lang="scss">
	footer {
		a {
			color: var(--text-secondary);

			&:hover {
				color: var(--text-primary);
				text-decoration: underline;
			}
		}
	}
</style>