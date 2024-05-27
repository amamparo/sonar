import { redirect } from '@sveltejs/kit';

export async function load() {
	const redirectUri = `${import.meta.env.VITE_SPOTIFY_REDIRECT_URI_BASE_URL}/auth/callback`;
	redirect(
		302,
		[
			'https://accounts.spotify.com/authorize?response_type=token',
			`&client_id=${import.meta.env.VITE_SPOTIFY_CLIENT_ID}`,
			`&scope=${encodeURIComponent(
				[
					'user-read-private',
					'user-read-email',
					'playlist-modify-public',
					'playlist-modify-private',
					'playlist-read-private'
				].join(' ')
			)}`,
			`&redirect_uri=${encodeURIComponent(redirectUri)}`,
			`&show_dialog=true`
		].join('')
	);
}
