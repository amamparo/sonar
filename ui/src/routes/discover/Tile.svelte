<script lang="ts">
	let className: string | undefined | null = undefined;
	export { className as class };
	export let title: string | null = null;
</script>

<div class="bg-foreground rounded-lg p-4 text-secondary {className}">
	{#if title}
		<div class="font-circular-bold text-lg pb-3">{title}</div>
	{/if}
	<slot />
</div>