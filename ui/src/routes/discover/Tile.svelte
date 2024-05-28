<script lang="ts">
	let className: string | undefined | null = undefined;
	export { className as class };
</script>

<div class="bg-midground rounded-lg p-2.5 pt-2 text-secondary {className}">
	<div class="flex justify-between items-center font-circular-bold text-lg pb-3 pl-2">
		<slot name="header" />
	</div>
	<slot />
</div>