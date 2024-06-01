<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import tokenManager from '$lib/tokenManager';

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
	<h1>Welcome to SvelteKit</h1>
	<p>Visit <a href="https://kit.svelte.dev">kit.svelte.dev</a> to read the documentation</p>

	<a class="text-white" href="/login">Go</a>
{/if}