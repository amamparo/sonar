import { type Subscriber, type Unsubscriber, type Updater, writable } from 'svelte/store';
import type { Track } from '$lib/models';

const KEY = 'tracks';

type TracksState = {
	isUpdating: boolean,
	tracks: Track[],
}

class Tracks {
	public readonly subscribe: (subscriber: Subscriber<TracksState>) => Unsubscriber;
	private readonly update: (updater: Updater<TracksState>) => void;

	constructor() {
		const store = writable<TracksState>({
			isUpdating: false,
			tracks: JSON.parse(localStorage.getItem(KEY) || '[]')
		});
		this.subscribe = store.subscribe;
		this.update = store.update;
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

	private persist<T>(x: T): T {
		localStorage.setItem(KEY, JSON.stringify(x.tracks));
		x.isUpdating = false;
		return x;
	}
}

export default new Tracks();