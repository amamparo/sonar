<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import tokenManager from '$lib/tokenManager.ts';

	onMount(async () => {
		const code = new URLSearchParams(window.location.search).get('code')
		await tokenManager.fetchRefreshToken(code)
		goto('/discover');
	});
</script>