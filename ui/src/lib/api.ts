import type { Playlist, Track } from './models';
import tokenManager from '$lib/tokenManager';

export const redirectUri = `${import.meta.env.VITE_SPOTIFY_REDIRECT_URI_BASE_URL}/login/callback`

class Api {
	async exportPlaylist(name: string, trackIds: string[]): Promise<void> {
		await this.post('/playlist', {
			name,
			trackIds
		})
	}

	async getTracks(trackIds: string[]): Promise<Track[]> {
		const response = await this.post('/tracks', trackIds)
		return response || []
	}

	async searchPlaylists(query: string): Promise<Playlist[]> {
		const response = await this.get(`/search/playlists/${query}`);
		return response || [];
	}

	async getPlaylistTracks(playlistId: string): Promise<Track[]> {
		const response = await this.get(`/playlist/${playlistId}/tracks`);
		return response || [];
	}

	async searchTracks(query: string): Promise<Track[]> {
		const response = await this.get(`/search/tracks/${query}`);
		return response || [];
	}

	async getRecommendations(track_ids: string[], signal: AbortSignal): Promise<Track[]> {
		return this.post('/recommendations', track_ids, signal);
	}

	private async post(path: string, data: any, signal?: AbortSignal) {
		return this.request({method: 'POST', path, data, signal});
	}

	private async get(path: string, params?: object) {
		return this.request({method: 'GET', path, params});
	}

	private async request(props: { method: string, path: string, data?: any, params?: object, signal?: AportSignal }) {
		const { method, path, data, params, signal } = props;
		const url = `${import.meta.env.VITE_API_BASE_URL}${path}${params ? '?' + new URLSearchParams(params).toString() : ''}`;
		const fetchOptions: RequestInit = {
			method,
			headers: {
				'Content-Type': 'application/json'
			}
		};
		const token = await tokenManager.getAccessToken()
		if (token) {
			fetchOptions.headers!['token'] = token
		}
		if (data) {
			fetchOptions.body = JSON.stringify(data);
		}
		if (signal) {
			fetchOptions.signal = signal;
		}
		const response = await fetch(url, fetchOptions);
		if (response.status > 400 && response.status <= 403) {
			window.location.href = '/login';
		} else if (response.status == 404) {
			return null;
		}
		return response.json();
	}
}

export default new Api();
