/** @type {import('tailwindcss').Config} */
export default {
	darkMode: 'class',
	content: ['./src/**/*.{html,js,svelte,ts}'],
	theme: {
		extend: {
			colors: {
				background: 'var(--background)',
				foreground: 'var(--foreground)',
				primary: 'var(--text-primary)',
				secondary: 'var(--text-secondary)',
			},
		},
	},
	plugins: [require('@tailwindcss/typography')]
}