import type { Track } from './models';

export type PlaylistSearchResult = {
	id: string;
	title: string;
	author: string;
	imageUrl: string;
}

class Api {
	private static readonly SPOTIFY_TOKEN = 'spotify_token';

	async searchPlaylists(query: string): Promise<PlaylistSearchResult[]> {
		const response = await this.get(`/search/playlists/${query}`);
		if (!response) {
			return [];
		}
		return response.map((item: object) => ({
			id: item.id,
			title: item.title,
			author: item.author,
			imageUrl: item.image_url
		}));
	}

	async playlistTracks(playlistId: string): Promise<Track[]> {
		const response = await this.get(`/playlist/${playlistId}/tracks`);
		if (!response) {
			return [];
		}
		return response.map((item: object) => ({
			id: item.id,
			title: item.title,
			artist: item.artist,
			album: item.album,
			previewUrl: item.preview_url,
			imageUrl: item.image_url
		}));
	}

	private async get(path: string) {
		const url = `${import.meta.env.VITE_API_BASE_URL}${path}`;
		const response = await fetch(url, {
			headers: {
				token: this.getToken() || ''
			}
		});
		if (response.status >= 400 && response.status <= 403) {
			window.location.href = '/auth';
		} else if (response.status == 404) {
			return null;
		}
		return response.json();
	}

	setToken(token: string) {
		localStorage.setItem(Api.SPOTIFY_TOKEN, token);
	}

	clearToken() {
		localStorage.removeItem(Api.SPOTIFY_TOKEN);
	}

	hasToken(): boolean {
		return this.getToken() !== null;
	}

	private getToken(): string | null {
		return localStorage.getItem(Api.SPOTIFY_TOKEN);
	}
}

export default new Api();
