import type { Playlist, Recommendations, Track } from './models';

class Api {
	private static readonly SPOTIFY_TOKEN = 'spotify_token';

	async searchPlaylists(query: string): Promise<Playlist[]> {
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

	async getPlaylistTracks(playlistId: string): Promise<Track[]> {
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

	async searchTracks(query: string): Promise<Track[]> {
		const response = await this.get(`/search/tracks/${query}`);
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

	async getRecommendations(tracks: Track[]): Promise<Recommendations> {
		const response = await this.post('/recommendations', tracks.map(track => track.id));
		return {
			inputAverageFeatures: response.input_average_features,
			recommendations: response.recommendations.map((item: object) => ({
				id: item.id,
				title: item.title,
				artist: item.artist,
				album: item.album,
				previewUrl: item.preview_url,
				imageUrl: item.image_url,
				features: item.features
			}))
		};

	}

	private async post(path: string, data: any) {
		return this.request('POST', path, data);
	}

	private async get(path: string) {
		return this.request('GET', path);
	}

	private async request(method: string, path: string, data?: any) {
		const url = `${import.meta.env.VITE_API_BASE_URL}${path}`;
		const fetchOptions: RequestInit = {
			method,
			headers: {
				token: this.getToken() || ''
			}
		};
		if (data) {
			fetchOptions.headers!['Content-Type'] = 'application/json';
			fetchOptions.body = JSON.stringify(data);
		}
		const response = await fetch(url, fetchOptions);
		if (response.status >= 400 && response.status <= 403) {
			window.location.href = '/login';
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
