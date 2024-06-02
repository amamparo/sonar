<script>
	import { createEventDispatcher, onMount } from 'svelte';

	const dispatch = createEventDispatcher();

	const close = () => dispatch('close');

	const handleKeydown = event => {
		if (event.key === 'Escape' || event.key === 'Esc') {
			close();
		}
	};

	onMount(() => {
		window.addEventListener('keydown', handleKeydown);

		return () => {
			window.removeEventListener('keydown', handleKeydown);
		};
	});
</script>

<div class="fixed inset-0 flex items-center justify-center z-50">
	<div class="fixed inset-0 bg-background opacity-40" on:click={close}></div>
	<div class="relative bg-foreground flex items-center justify-center z-10 p-4 rounded w-1/4">
		<div class="flex flex-col w-full">
			<slot />
		</div>
	</div>
</div>