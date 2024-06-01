<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import tokenManager from '$lib/tokenManager';

	onMount(() => {
		tokenManager.clear()
		goto('/')
	})
</script>