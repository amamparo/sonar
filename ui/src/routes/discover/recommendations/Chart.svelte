<script context="module">
	import ApexCharts from 'apexcharts';

	import { previewPlayer } from '$lib';
</script>

<script lang="ts">
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

	export let recommendations;

	export let clearSelections = () => {
		const copy = [...selectedDataPointIndexes];
		for (const index of copy) {
			myChart.toggleDataPointSelection(0, index);
		}
	}

	export let setSelectedTracks = () => {};

	let selectedDataPointIndexes = [];

	export let selectedTracks;

	let hoveredTrack = null;

	$: if (hoveredTrack != null) {
		previewPlayer.play(hoveredTrack);
	} else {
		previewPlayer.stop();
	}

	const axisOptions = {
		type: 'numeric',
		tickAmount: 5,
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
			height: '100%',
			width: '100%',
			animations: {
				enabled: false
			},
			selection: {
				enabled: false
			},
			toolbar: {
				show: true,
				tools: {
					reset: true,
					zoom: true,
					zoomin: false,
					zoomout: false,
					pan: false,
					download: false,
					selection: false
				}
			},
			zoom: {
				enabled: true,
				type: 'xy',
				autoScaleYaxis: true
			},
			events: {
				dataPointMouseEnter: (event, chartContext, config) => {
					const track = recommendations.recommendations[config.dataPointIndex];
					if (hoveredTrack == null || track.id !== hoveredTrack.id) {
						hoveredTrack = track;
					}
				},
				dataPointMouseLeave: (event, chartContext, config) => {
					hoveredTrack = null;
				},
				dataPointSelection: (event, chartContext, config) => {
					selectedDataPointIndexes = config.selectedDataPoints[0];
					setSelectedTracks(selectedDataPointIndexes.map((index) => recommendations.recommendations[index]));
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
			size: 7,
			hover: {
				sizeOffset: 4
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
				const track = recommendations.recommendations[recommendationIndex];
				return `
					<div class="flex items-center p-2.5 bg-foreground max-w-96">
						<div class="relative w-12 h-12 flex-none rounded overflow-hidden">
							<img src="${track.imageUrl}" class="absolute" />
						</div>
						<div class="flex flex-col flex-1 ms-3 overflow-hidden">
							<div class="text-base text-primary truncate">${track.title}</div>
							<div class="text-sm text-secondary truncate">${track.artist}</div>
						</div>
					</div>
				`;
			}
		}
	};

	$: options.series = [{
		data: recommendations?.recommendations.map((track) => ({
			x: track.features.energy,
			y: track.features.valence
		}))
	}];
</script>

<div use:chart={options} class="z-0" />

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
          fill: royalblue;
          stroke: royalblue;
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