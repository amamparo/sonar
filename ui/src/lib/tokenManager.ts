import { redirectUri } from '$lib/api';
import _ from 'lodash';
import { SPOTIFY_CLIENT_ID } from '$lib/env';

const ACCESS_TOKEN = 'access_token'
const REFRESH_TOKEN = 'refresh_token'
const EXPIRES_AT = 'expires_at'

class TokenManager {
	hasAccessToken() {
		return localStorage.hasOwnProperty('access_token');
	}

	clear() {
		localStorage.removeItem(ACCESS_TOKEN);
		localStorage.removeItem(REFRESH_TOKEN);
		localStorage.removeItem(EXPIRES_AT);
	}

	async getAccessToken(): Promise<string | null> {
		let accessToken = localStorage.getItem(ACCESS_TOKEN)
		const expiresAt = localStorage.getItem(EXPIRES_AT)
		if (accessToken && expiresAt && this.now() < Number(expiresAt)) {
			return accessToken;
		}

		const refreshToken = localStorage.getItem(REFRESH_TOKEN)
		if (refreshToken) {
			const url =`${import.meta.env.VITE_API_BASE_URL}/token/refresh?refreshToken=${refreshToken}`;
			const { accessToken, expiresIn } = await (
				await fetch(url, { method: 'GET' })
			).json()
			localStorage.setItem(ACCESS_TOKEN, accessToken)
			localStorage.setItem(EXPIRES_AT, this.now() + expiresIn)
			return accessToken
		}

		return null;
	}

	async fetchRefreshToken(code: string) {
		const url = `${import.meta.env.VITE_API_BASE_URL}/token?code=${code}&redirectUri=${encodeURIComponent(redirectUri)}`;
		const { accessToken, refreshToken, expiresIn } = await (
			await fetch(url, { method: 'GET' })
		).json();
		localStorage.setItem(ACCESS_TOKEN, accessToken)
		localStorage.setItem(REFRESH_TOKEN, refreshToken)
		localStorage.setItem(EXPIRES_AT, this.now() + expiresIn)
	}

	private now(): number {
		return _.floor(new Date().getTime() / 1000);
	}
}

export default new TokenManager();