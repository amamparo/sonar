<script lang="ts">
	let className: string | undefined | null = undefined;
	export { className as class };
</script>

<div class="bg-foreground rounded-lg p-4 text-secondary {className}">
	<slot />
</div>