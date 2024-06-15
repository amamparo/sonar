<script lang="ts">
	import { onMount } from 'svelte';
	import Playlist from './playlist/Playlist.svelte';
	import { goto } from '$app/navigation';
	import Logout from '$lib/components/icon/Logout.svelte';
	import Recommendations from './recommendations/Recommendations.svelte';
	import tokenManager from '$lib/tokenManager';

	let isMobile = false;

	onMount(() => {
		if (!tokenManager.hasAccessToken()) {
			window.location.href = '/login';
		}

		const userAgent = navigator.userAgent || navigator.vendor || window.opera;
		isMobile = /Mobi|Android|iPhone/i.test(userAgent);
	});
</script>

<body class="bg-background min-h-screen font-circular-medium">
{#if isMobile}
	<div class="text-white text-xl min-h-screen font-circular-medium flex items-center justify-center mx-8">
		Sorry!  Sonar isn't available on mobile devices (yet). Please visit on a desktop or tablet.
	</div>
{:else}
	<div class="max-w-screen-3xl mx-auto">
		<div class="flex flex-col h-screen space-y-3 p-3">
			<div class="w-full bg-midground text-primary p-2 flex justify-between items-center rounded">
				<div class="text-lg pl-4 font-circular-bold">
					Sonar
				</div>
				<button class="w-8 h-8 p-2 fill-secondary hover:fill-red-600" title="Sign Out" on:click={() => goto('/logout')}>
					<Logout />
				</button>
			</div>
			<div class="flex-grow overflow-hidden flex">
				<div class="space-x-3 w-full flex">
					<Playlist />
					<Recommendations />
				</div>
			</div>
			<footer class="mx-auto text-muted font-circular-book text-sm">
				Copyright &copy; {new Date().getFullYear()} Sonar
				&nbsp;|&nbsp;
				Created by <a href="https://aaronmamparo.com" target="_blank">Aaron Mamparo</a>
				&nbsp;|&nbsp;
				<a href="mailto:aaronmamparo@gmail.com">Feedback?</a>
			</footer>
		</div>
	</div>
{/if}
</body>

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