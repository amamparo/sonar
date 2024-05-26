<script lang="ts">
	import { api } from '$lib';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';

	onMount(() => {
		api.clearToken()
		goto('/')
	})
</script>