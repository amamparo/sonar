<script lang="ts">
	import type { SvelteComponent } from 'svelte';

	export let icon: SvelteComponent;
	export let text: string;
	export let action: (() => void) | null = null;
	export let subMenu: SvelteComponent | null = null;

	export let subMenuToShow;
	export let closeParentMenu: () => void;

	$: buttonClass = subMenu && subMenuToShow === subMenu ? 'bg-highlight' : '';

	const wrap = innerAction => {
		if (innerAction) {
			closeParentMenu();
			innerAction();
		}
	}
</script>

<li>
	<div class="relative">
		<button class="flex gap-3.5 w-full text-start items-center p-2.5 px-3 rounded
		hover:bg-highlight {buttonClass}"
						on:click={wrap(action)} on:pointerenter={() => {
							subMenuToShow = subMenu;
						}}>
			<svelte:component this={icon} />
			<span>{text}</span>
		</button>
	</div>
</li>

<style lang="scss">
  button :global(svg) {
    width: 16px;
    height: 16px;
    fill: var(--text-secondary);
  }
</style>
