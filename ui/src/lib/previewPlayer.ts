import { type Subscriber, type Writable, writable } from 'svelte/store';
import type { Track } from '$lib/models';

type State = {
	currentTrack: Track | null;
	currentDuration: number;
}

class PreviewPlayer {
	private readonly audio = new Audio();
	private readonly store: Writable<State> = writable({});
	private currentState: State;

	constructor() {
		this.audio.onended = () => {
			this.store.update(state => {
				state.currentTrack = null;
				return state;
			});
		}

		this.audio.addEventListener('loadedmetadata', () => {
			this.store.update(state => {
				state.currentDuration = this.audio.duration;
				return state;
			})
		})

		this.store.subscribe(state => {
			this.currentState = state;
		})
	}

	subscribe(run: Subscriber<State>) {
		this.store.subscribe(run);
	}

	play(track: Track) {
		this.store.update(state => {
			state.currentTrack = track;
			return state;
		})
		this.audio.src = track.previewUrl;
		this.audio.play();
	}

	stop() {
		this.audio.pause();
		this.audio.currentTime = 0;
		this.store.update(state => {
			state.currentTrack = null;
			return state;
		});
	}

	toggle(track: Track) {
		if (this.currentState.currentTrack === track) {
			this.stop();
		} else {
			this.play(track)
		}
	}
}

export default new PreviewPlayer();