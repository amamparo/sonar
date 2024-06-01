<script context="module">
	import ApexCharts from 'apexcharts';

	import { previewPlayer } from '$lib';
</script>

<script lang="ts">
	import Button from '$lib/components/Button.svelte';
	import { trackStore } from '$lib';
	import AxisSelect from './AxisSelect.svelte';
	import _ from 'lodash';
	import { onMount } from 'svelte';
	import features from './features';
	import { Stats } from 'fast-stats';

	export let recommendations;

	let xAxisFeature;
	let yAxisFeature;
	let isZoomed = false;

	onMount(() => {
		if ((recommendations || []).length === 0) {
			return [];
		}
		const featureOptimalnesses = features.reduce((accum, featureKey) => {
			const featureValues = recommendations.map(({ features }) => features[featureKey]);
			const stats = new Stats().push(featureValues);
			const mean = stats.amean();
			const stddev = stats.stddev();
			const zScores = featureValues.map(x => Math.abs(x - mean) / stddev);
			const maxZScore = Math.max(...zScores);
			return {
				...accum,
				[featureKey]: -maxZScore
			};
		}, {});
		const featuresSortedByOptimalness = _.sortBy(
			Object.entries(featureOptimalnesses),
			([_, optimalness]) => optimalness
		).map(([key, _]) => key).reverse();
		xAxisFeature = featuresSortedByOptimalness[0];
		yAxisFeature = featuresSortedByOptimalness[1];
	});

	let selectedDataPointIndexes = [];

	let selectedTracks = [];

	$: if (selectedTracks.length === 0) {
		const copy = [...selectedDataPointIndexes];
		for (const index of copy) {
			myChart.toggleDataPointSelection(0, index);
		}
	}

	let myChart;
	const chart = (node, options) => {
		myChart = new ApexCharts(node, options);
		myChart.render();

		return {
			update(options) {
				myChart.updateOptions(options);
			}
		};
	};

	const axisOptions = {
		type: 'numeric',
		tickAmount: 6,
		min: 0,
		max: 1,
		axisBorder: {
			show: false
		},
		axisTicks: {
			show: false
		},
		crosshairs: {
			show: false
		},
		labels: {
			show: false
		}
	};

	let options = {
		chart: {
			type: 'scatter',
			width: '100%',
			height: '100%',
			offsetX: -7,
			offsetY: -15,
			animations: {
				enabled: false
			},
			selection: {
				enabled: false
			},
			toolbar: {
				show: false
			},
			zoom: {
				enabled: true,
				type: 'xy',
				autoScaleYaxis: true
			},
			events: {
				dataPointMouseEnter: (event, chartContext, config) => {
					const track = recommendations[config.dataPointIndex];
					previewPlayer.play(track);
				},
				dataPointMouseLeave: () => {
					previewPlayer.stop();
				},
				dataPointSelection: (event, chartContext, config) => {
					selectedDataPointIndexes = config.selectedDataPoints[0];
					selectedTracks = selectedDataPointIndexes.map((index) => recommendations[index])
				},
				mounted: () => {
					myChart.updateOptions({
						chart: {
							height: '100%'
						}
					});
				},
				zoomed: (chartContext, { xaxis, yaxis }) => {
					isZoomed = true;
				}
			}
		},
		states: {
			active: {
				allowMultipleDataPointsSelection: true,
				filter: {
					type: 'none'
				}
			}
		},
		grid: {
			xaxis: {
				lines: {
					show: true
				}
			},
			yaxis: {
				lines: {
					show: true
				}
			}
		},
		legend: {
			show: false
		},
		markers: {
			size: 8,
			hover: {
				sizeOffset: 3
			},
			strokeWidth: 1
		},
		xaxis: axisOptions,
		yaxis: axisOptions,
		tooltip: {
			enabled: true,
			x: {
				show: false
			},
			y: {
				show: false
			},
			marker: {
				show: false
			},
			theme: 'dark',
			custom: ({ dataPointIndex: recommendationIndex }) => {
				const track = recommendations[recommendationIndex];
				return `
					<div class="flex items-center p-2.5 bg-foreground max-w-96">
						<div class="relative w-12 h-12 flex-none rounded overflow-hidden">
							<img src="${track.imageUrl}" class="absolute" />
						</div>
						<div class="flex flex-col flex-1 ms-3 overflow-hidden">
							<div class="text-base text-primary truncate">${track.title}</div>
							<div class="text-sm text-secondary truncate">
								${track.artists.map(x => x.name).join(', ')}
							</div>
						</div>
					</div>
				`;
			}
		}
	};

	$: {
		const x = (recommendations || []).map(({ features }) => features[xAxisFeature]);
		const y = (recommendations || []).map(({ features }) => features[yAxisFeature]);
		const minX = _.min(x);
		const rangeX = _.max(x) - minX;
		const minY = _.min(y);
		const rangeY = _.max(y) - minY;
		options.series = [{
			data: _.zip(x, y).map(([x, y]) => {
				return {
					x: (x - minX) / rangeX,
					y: (y - minY) / rangeY
				};
			})
		}];
	}

	const addSelections = () => {
		trackStore.addAll(selectedTracks);
		selectedTracks = [];
	};

	const resetZoom = () => {
		myChart.resetSeries();
		isZoomed = false;
	};

	$: if (xAxisFeature && yAxisFeature) {
		resetZoom();
	}
</script>

<div class="flex flex-col h-full">
	<div class="w-full px-4 flex z-10 space-x-10 flex-0">
		<AxisSelect axis="X" bind:featureValue={xAxisFeature} bind:otherFeatureValue={yAxisFeature} />
		<AxisSelect axis="Y" bind:featureValue={yAxisFeature} bind:otherFeatureValue={xAxisFeature} />
		{#if isZoomed}
			<Button class="text-sm text-secondary hover:text-primary hover:border-primary"
							onClick={resetZoom}>
				Reset Zoom
			</Button>
		{/if}
	</div>
	<div class="w-full flex-grow">
		<div use:chart={options} class="z-0" />
	</div>
	<div class="items-center justify-center mx-auto p-0 pb-5 space-x-2">
		{#if selectedTracks && selectedTracks.length > 0}
			<Button onClick={addSelections} class="hover:border-spotify-green hover:text-spotify-green">
				Add {selectedTracks.length} Track{selectedTracks.length > 1 ? 's' : ''}
			</Button>
			<Button onClick={() => selectedTracks = []} class="hover:border-red-600 hover:text-red-600">
				Clear Selection
			</Button>
		{:else}
			<span class="text-muted font-circular-book">Click on recommendations to queue them for your playlist.</span>
		{/if}
	</div>
</div>

<style lang="scss">
  :global {
    .apexcharts-gridline {
      stroke: var(--text-muted);
    }

    .apexcharts-series-markers {
      circle {
        stroke: var(--spotify-green);
        fill: var(--spotify-green);
        opacity: 0.7;

        &[selected="true"] {
          fill: dodgerblue;
          stroke: dodgerblue;
        }
      }

      &:hover {
        cursor: pointer;
      }
    }

    .apexcharts-zoom-icon {
      display: none;
    }

    .apexcharts-xaxistooltip {
      display: none;
    }
  }
</style>