<script>
	import _ from 'lodash';
	import features from './features';

	export let axis;
	export let featureValue;
	export let otherFeatureValue;
</script>

<div class="text-sm">
	<span class="pr-1">{axis}</span>
	<select bind:value={featureValue} class="bg-foreground p-1">
		{#each features as feature}
			<option value={feature} disabled={feature === otherFeatureValue}>
				{_.capitalize(feature)}
			</option>
		{/each}
	</select>
</div>