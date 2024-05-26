<script lang="ts">
	import { api } from '$lib';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';

	let checkingToken = true;

	onMount(() => {
		if (api.hasToken()) {
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

	<a href="/discover">Go</a>
{/if}