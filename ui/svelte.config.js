import adapter from '@sveltejs/adapter-static'
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte'
import sveltePreprocess from 'svelte-preprocess'

const config = {
	preprocess: [
		vitePreprocess(),
		sveltePreprocess({
			scss: true,
			typescript: true
		})
	],
	extensions: ['.svelte'],
	kit: {
		adapter: adapter({
			pages: 'build',
			assets: 'build',
			fallback: 'index.html',
			precompress: false,
			strict: true,
			trailingSlash: 'always'
		})
	}
}

export default config
