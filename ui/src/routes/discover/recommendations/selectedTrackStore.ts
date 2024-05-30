import { writable } from 'svelte/store';

const { subscribe, set } = writable([])

export default {
	subscribe,
	setAll: tracks => set(tracks),
	clear: () => set([])
};