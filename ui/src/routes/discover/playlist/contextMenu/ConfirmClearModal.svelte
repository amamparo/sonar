<script>
	import { createEventDispatcher } from 'svelte';
	import Button from '$lib/components/Button.svelte';
	import { trackStore } from '$lib';
	import Modal from '$lib/components/Modal.svelte';

	const dispatch = createEventDispatcher();

	const close = () => dispatch('close');

	const confirm = () => {
		trackStore.clear();
		close();
	};
</script>

<Modal on:close={close}>
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
</Modal>
