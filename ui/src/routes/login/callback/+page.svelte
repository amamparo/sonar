<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import tokenManager from '$lib/tokenManager.ts';

	onMount(async () => {
		const params = new URLSearchParams(window.location.search)
		console.log(">>> " + params)
		const error = params.get('error')
		if (error && error === 'access_denied') {
			return goto('/');
		}
		const code = params.get('code')
		await tokenManager.fetchRefreshToken(code)
		return goto('/discover');
	});
</script>