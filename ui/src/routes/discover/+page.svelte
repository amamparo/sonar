<script lang="ts">
	import { onMount } from 'svelte';
	import { api } from '$lib';

	onMount(() => {
		if (!api.hasToken()) {
			window.location.href = '/auth';
		}
	});
</script>

<main>
	<!-- Your content here -->
</main>