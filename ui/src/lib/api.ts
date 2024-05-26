class Api {
	private static readonly SPOTIFY_TOKEN = 'spotify_token';

	async get(path: string) {
		const url = `${import.meta.env.VITE_API_BASE_URL}${path}`;
		const response = await fetch(url, {
			headers: {
				token: this.getToken() || '',
			}
		});
		if (response.status >= 400 && response.status < 500) {
			window.location.href = '/auth'
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
