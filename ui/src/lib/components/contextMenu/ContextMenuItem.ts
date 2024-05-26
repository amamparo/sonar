import type { SvelteComponent } from 'svelte';

type ContextMenuItem = {
	icon: SvelteComponent;
	text: string;
	action: () => void;
};

export default ContextMenuItem;
