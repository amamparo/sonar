<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import tokenManager from '$lib/tokenManager';
	import Button from '$lib/components/Button.svelte';

	let checkingToken = true;

	onMount(() => {
		if (tokenManager.hasAccessToken()) {
			goto('/discover');
		}
		checkingToken = false;
	});
</script>

{#if checkingToken}
	<!-- wait -->
{:else}
	<div class="main min-h-screen font-circular-medium flex items-center justify-center">
		<div class="text-center space-y-8 font-circular-black px-4 lg:px-16 3xl:px-24 w-full xl:w-2/3 3xl:w-1/2">
			<div class="mx-auto">
				<img src="/screenshot.png" class="max-h-[60vh] mx-auto"/>
			</div>
			<div class="text-white text-2xl lg:text-3xl">
				Create better Spotify playlists with Sonar, a song recommendation tool that uses audio analysis and
				visualization to help you curate the perfect vibe.
			</div>
			<div>
				<Button class="bg-spotify-green border-none font-circular-bold text-xl px-8 py-2 rounded-3xl"
								on:click={() => goto("/login")}>
					Get Started
				</Button>
			</div>
		</div>
	</div>
{/if}

<style lang="scss">
  .main {
    background-image: linear-gradient(rgb(30, 50, 100) 0px, rgb(18, 18, 18) 40%);
  }
</style>