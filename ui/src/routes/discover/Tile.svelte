<script lang="ts">
	let className: string | undefined | null = undefined;
	export { className as class };
</script>

<div class="bg-midground rounded-lg p-4 pt-3 text-secondary {className}">
	<div class="flex justify-between items-center font-circular-bold text-lg pb-3">
		<slot name="header" />
	</div>
	<slot />
</div>