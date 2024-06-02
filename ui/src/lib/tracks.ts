import { writable } from 'svelte/store';

const KEY = 'tracks';

const { subscribe, update } = writable({
	isUpdating: false,
	tracks: JSON.parse(localStorage.getItem(KEY) || '[]')
})

const persist = x => {
	localStorage.setItem(KEY, JSON.stringify(x.tracks));
	x.isUpdating = false;
	return x;
}

export default {
	subscribe,
	setAll: tracks => update(x => {
		x.tracks = tracks;
		return persist(x);
	}),
	delete: trackId => update(x => {
		x.tracks = x.tracks.filter(t => t.id !== trackId);
		return persist(x);
	}),
	clear: () => update(x => {
		x.tracks = [];
		return persist(x);
	}),
	addAll: tracks => update(x => {
		const newTracks = tracks.filter(track => !x.tracks.some(t => t.id === track.id));
		x.tracks = [...x.tracks, ...newTracks];
		return persist(x);
	}),
	setUpdating: isUpdating => update(x => {
		x.isUpdating = isUpdating;
		return x;
	})
};