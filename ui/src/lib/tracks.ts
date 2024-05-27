import { type Subscriber, type Writable, writable } from 'svelte/store';
import type { Track } from './models';

const KEY = 'tracks';

class State {
	public isUpdating: boolean;
	public tracks: Track[];

	constructor(tracks: Track[]) {
		this.tracks = tracks;
		this.isUpdating = false;
	}
}

class TrackStore {
	private state: State;
	private readonly store: Writable<State>;

	constructor() {
		const stored = localStorage.getItem(KEY);
		this.state = new State(stored ? JSON.parse(stored) : []);
		this.store = writable(this.state);
	}

	public subscribe(run: Subscriber<State>) {
		this.store.subscribe(run);
	}

	public setAll(tracks: Track[]) {
		this.store.update(state => {
			state.tracks = tracks;
			return state;
		});
		this.save();
	}

	public delete(trackId: string) {
		this.store.update(state => {
			state.tracks = state.tracks.filter(track => track.id !== trackId);
			return state;
		});
		this.save();
	}

	public add(track: Track) {
		if (this.state.tracks.some(t => t.id === track.id)) {
			return;
		}
		this.store.update(state => {
			state.tracks = [...state.tracks, track];
			return state;
		});
		this.save();
	}

	public clear() {
		this.setAll([]);
	}

	public setUpdating(isUpdating: boolean) {
		this.store.update(state => {
			state.isUpdating = isUpdating;
			return state;
		});
	}

	private save() {
		localStorage.setItem(KEY, JSON.stringify(this.state.tracks));
		this.setUpdating(false);
	}
}

export default new TrackStore();
