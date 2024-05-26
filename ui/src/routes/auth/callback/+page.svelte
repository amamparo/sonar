<script>
	import { api } from '$lib';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';

	onMount(() => {
		api.setToken(new URLSearchParams(window.location.hash.replace('#', '')).get('access_token'));
		goto('/discover');
	});
</script>