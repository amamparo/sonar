export type AudioFeatures = {
	acousticness: number;
	danceability: number;
	energy: number;
	instrumentalness: number;
	liveness: number;
	speechiness: number;
	valence: number;
}

export type Track = {
	id: string;
	title: string;
	artist: string;
	album: string;
	imageUrl: string;
	previewUrl: string;
	features?: AudioFeatures;
};

export type Recommendations = {
	inputAverageFeatures: AudioFeatures;
	recommendations: Track[];
}

export type Playlist = {
	id: string;
	title: string;
	author: string;
	imageUrl: string;
};
