/** @type {import('tailwindcss').Config} */
export default {
	darkMode: 'class',
	content: ['./src/**/*.{html,js,svelte,ts}'],
	theme: {
		extend: {
			colors: {
				background: 'var(--background)',
				foreground: 'var(--foreground)',
				'input-background': 'var(--input-background)',
				primary: 'var(--text-primary)',
				secondary: 'var(--text-secondary)',
				'spotify-green': 'var(--spotify-green)'
			},
		},
	},
	plugins: [require('@tailwindcss/typography')]
}