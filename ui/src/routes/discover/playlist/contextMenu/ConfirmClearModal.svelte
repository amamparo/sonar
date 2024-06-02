<script>
	import { createEventDispatcher, onMount } from 'svelte';
	import Button from '$lib/components/Button.svelte';
	import { trackStore } from '$lib';

	const dispatch = createEventDispatcher();

	const close = () => dispatch('close');

	const confirm = () => {
		trackStore.clear();
		close();
	}

	const handleKeydown = event => {
		if (event.key === 'Escape' || event.key === 'Esc') {
			close();
		}
	}

	onMount(() => {
		window.addEventListener('keydown', handleKeydown);

		return () => {
			window.removeEventListener('keydown', handleKeydown);
		};
	});
</script>

<div class="fixed inset-0 flex items-center justify-center z-50">
	<div class="fixed inset-0 bg-background opacity-50" on:click={close}></div>
	<div class="relative bg-foreground flex items-center justify-center z-10 p-5 rounded">
		<div class="flex flex-col">
			<span class="text-light font-circular-book">
				Are you sure you want to delete all tracks?
			</span>
			<div class="flex w-full mt-4 justify-end space-x-3">
				<Button class="border-secondary text-secondary hover:border-primary hover:text-primary"
								on:click={close}>
					Cancel
				</Button>
				<Button class="border-secondary text-secondary hover:border-primary hover:text-primary"
								on:click={confirm}>
					Confirm
				</Button>
			</div>
		</div>
	</div>
</div>