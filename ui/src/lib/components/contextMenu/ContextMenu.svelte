<script lang="ts">
	import Ellipsis from './Ellipsis.svelte';
	import { onMount } from 'svelte';
	import ContextMenuItem from './ContextMenuItem.svelte';

	export let items: object[] = [];

	export let menuClass = '';

	export let showMenu = false;
	let button;
	let menu;

	export let subMenuToShow = null;

	const toggleMenu = () => {
		showMenu = !showMenu;
		if (subMenuToShow) {
			subMenuToShow = null;
		}
	}

	const closeMenu = () => {
		showMenu = false;
		subMenuToShow = null;
	};

	$: showMenu = showMenu || subMenuToShow !== null;

	const handleClickOutside = event => {
		if (menu && !menu.contains(event.target) && !button.contains(event.target)) {
			closeMenu();
		}
	};

	onMount(() => {
		document.addEventListener('pointerdown', handleClickOutside);
		return () => document.removeEventListener('pointerdown', handleClickOutside);
	});
</script>

<div class="relative">
	<button class="ellipsis rounded-lg p-2" bind:this={button} on:click={toggleMenu}>
		<Ellipsis />
	</button>
	{#if showMenu}
		<div class="absolute right-0 mt-2
				bg-foreground shadow-2xl rounded
				font-circular-book text-primary text-sm font-extralight
				{menuClass}" bind:this={menu}>
			<ul class="p-1">
				{#each items as item}
					<div class="relative">
						<ContextMenuItem {...item} closeParentMenu={closeMenu}
														 bind:subMenuToShow={subMenuToShow} />
						{#if item.subMenu && item.subMenu === subMenuToShow}
							<div class="absolute left-full top-0 ml-2 rounded shadow-xl bg-foreground">
								<svelte:component this={item.subMenu} onComplete={closeMenu} />
							</div>
						{/if}
					</div>
				{/each}
			</ul>
		</div>
	{/if}
</div>

<style lang="scss">
  button.ellipsis {
    &:hover {
      cursor: pointer;

      :global(svg) {
        fill: var(--text-primary);
      }
    }
  }

  button :global(svg) {
    width: 16px;
    height: 16px;
    fill: var(--text-secondary);
  }
</style>
