/** @type {import('tailwindcss').Config} */
export default {
	darkMode: 'class',
	content: ['./src/**/*.{html,js,svelte,ts}'],
	theme: {
		extend: {
			colors: {
				// background colors
				background: 'var(--background)',
				midground: 'var(--midground)',
				foreground: 'var(--foreground)',
				highlight: 'var(--highlight)',

				// text colors
				primary: 'var(--text-primary)',
				secondary: 'var(--text-secondary)',
				muted: 'var(--text-muted)',

				// misc colors
				'spotify-green': 'var(--spotify-green)'
			},
			screens: {
				'3xl': '2048px'
			}
		},
	},
	plugins: [require('@tailwindcss/typography')]
}