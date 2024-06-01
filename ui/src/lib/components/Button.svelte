<script lang="ts">
	import { createEventDispatcher } from 'svelte';

	const dispatch = createEventDispatcher()
	export let onClick = () => {
		dispatch('click')
	};

	let className: string | undefined | null = undefined;
	export { className as class };
</script>
<button class="text-primary text-sm font-circular-medium border-2 rounded-2xl px-4 py-1 {className}"
				data-modal-target="default-modal" data-modal-toggle="default-modal" on:click={onClick}>
	<slot/>
</button>

<style lang="postcss">
	button {
			border-color: rgb(114, 114, 114);
	}
</style>