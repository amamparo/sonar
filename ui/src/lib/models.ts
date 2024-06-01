export type AudioFeatures = {
	acousticness: number;
	danceability: number;
	energy: number;
	instrumentalness: number;
	liveness: number;
	loudness: number;
	speechiness: number;
	valence: number;
}

export type Artist = {
	id: string;
	name: string;
}

export type Track = {
	id: string;
	title: string;
	artists: Artist[];
	album: string;
	imageUrl: string;
	previewUrl: string;
	features?: AudioFeatures;
};

export type Playlist = {
	id: string;
	title: string;
	author: string;
	imageUrl: string;
};
