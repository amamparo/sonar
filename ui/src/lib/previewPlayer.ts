import { type Subscriber, type Writable, writable } from 'svelte/store';
import type { SvelteComponent } from 'svelte';

type State = {
	currentUrl: string | null;
	currentSource: string | null;
}

class PreviewPlayer {
	private readonly audio = new Audio();
	private readonly store: Writable<State> = writable({});
	private currentState: State;

	constructor() {
		this.audio.onended = () => {
			this.store.update(state => {
				state.currentUrl = null;
				state.currentSource = null;
				return state;
			});
		}

		this.store.subscribe(state => {
			this.currentState = state;
		})
	}

	subscribe(run: Subscriber<State>) {
		this.store.subscribe(run);
	}

	play(url: string, source: string) {
		this.store.update(state => {
			state.currentUrl = url;
			state.currentSource = source;
			return state;
		})
		this.audio.src = url;
		this.audio.play();
	}

	stop() {
		this.audio.pause();
		this.audio.currentTime = 0;
		this.store.update(state => {
			state.currentUrl = null;
			state.currentSource = null;
			return state;
		});
	}

	toggle(url: string, source: string) {
		if (this.currentState.currentSource === source) {
			this.stop();
		} else {
			this.play(url, source)
		}
	}
}

export default new PreviewPlayer();