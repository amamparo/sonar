class Api {
	private static readonly SPOTIFY_TOKEN = 'spotify_token'

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