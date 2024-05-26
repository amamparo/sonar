<script lang="ts">
	import Ellipsis from './Ellipsis.svelte';
	import { onMount } from 'svelte';
	import type ContextMenuItem from './ContextMenuItem.ts';

	export let items: ContextMenuItem[] = [];

	export let menuClass = ''

	let showMenu = false;
	let button;
	let menu;

	const toggleMenu = () => showMenu = !showMenu;

	const handleClickOutside = event => {
		if (menu && !menu.contains(event.target) && !button.contains(event.target)) {
			showMenu = false;
		}
	};

	onMount(() => {
		document.addEventListener('click', handleClickOutside);
		return () => document.removeEventListener('click', handleClickOutside);
	});

	const wrap = action => () => {
		showMenu = false;
		action();
	};
</script>

<div class="relative">
	<button class="ellipsis rounded-lg p-2" bind:this={button} on:click={toggleMenu}>
		<Ellipsis />
	</button>
	{#if showMenu}
		<div class="
		menu bg-foreground absolute right-0 mt-2 shadow-2xl rounded-sm
		font-circular-book text-primary text-sm font-extralight {menuClass}" bind:this={menu}>
			<ul class="p-1">
				{#each items as { icon, text, action }}
					<li>
						<button class="flex gap-3.5 w-full text-start items-center p-2.5 px-3 rounded-sm hover:bg-highlight"
										on:click={wrap(action)}>
							<svelte:component this={icon}/> <span>{text}</span>
						</button>
					</li>
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
