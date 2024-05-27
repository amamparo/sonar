<script lang="ts">
	export let onClick = () => {};
</script>
<button class="text-primary text-sm font-circular-medium border-2 rounded-2xl px-4 py-1 hover:border-secondary"
				data-modal-target="default-modal" data-modal-toggle="default-modal" on:click={onClick}><slot/></button>

<style lang="postcss">
	button {
			border-color: rgb(114, 114, 114);
	}
</style>