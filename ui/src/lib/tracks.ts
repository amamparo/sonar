import { type Subscriber, type Unsubscriber, type Updater, writable } from 'svelte/store';
import type { Track } from '$lib/models';
import api from '$lib/api';

const TRACK_IDS = 'track_ids';

type State = {
	isUpdating: boolean,
	tracks: Track[],
}

class Tracks {
	public readonly subscribe: (subscriber: Subscriber<State>) => Unsubscriber;
	private readonly update: (updater: Updater<State>) => void;

	constructor() {
		const store = writable<State>({
			isUpdating: true,
			tracks: []
		});
		this.subscribe = store.subscribe;
		this.update = store.update;

		const trackIds = JSON.parse(localStorage.getItem(TRACK_IDS) || '[]')
		api.getTracks(trackIds).then(tracks => store.update(x => {
			x.tracks = tracks;
			x.isUpdating = false;
			return x;
		}))
	}

	public setAll(tracks: Track[]): void {
		this.update(x => {
			x.tracks = tracks;
			return this.persist(x);
		});
	}

	public addAll(tracks: Track[]): void {
		this.update(x => {
			const newTracks = tracks.filter(track => !x.tracks.some(t => t.id === track.id));
			x.tracks = [...x.tracks, ...newTracks];
			return this.persist(x);
		});
	}

	public add(track: Track): void {
		this.addAll([track]);
	}

	public delete(trackId: string): void {
		this.update(x => {
			x.tracks = x.tracks.filter(t => t.id !== trackId);
			return this.persist(x);
		});
	}

	public clear(): void {
		this.setAll([]);
	}

	public setUpdating(isUpdating: boolean): void {
		this.update(x => {
			x.isUpdating = isUpdating;
			return x;
		});
	}

	private persist(x: State): State {
		localStorage.setItem(TRACK_IDS, JSON.stringify(x.tracks.map(t => t.id)));
		x.isUpdating = false;
		return x;
	}
}

export default new Tracks();