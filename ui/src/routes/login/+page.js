import { redirect } from '@sveltejs/kit';
import { SPOTIFY_CLIENT_ID } from '$lib/env.ts';
import { redirectUri } from '$lib/api.ts';

export async function load() {
	redirect(
		302,
		[
			'https://accounts.spotify.com/authorize?response_type=code',
			`&client_id=${SPOTIFY_CLIENT_ID}`,
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
