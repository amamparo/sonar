# TODO

## Must do before release
* UI updates to more closely match spotify UI
  * update track search result row to have "Add" pill button instead of plus icon
  * in track search and playlist view, use "Remove" pill button instead of trash icon
  * style "now playing" state of track being previewd
    * track title should be spotify green
    * track row should be highlighted (in a shade brighter than the hover highlight color)
    * adjust dimensions of play/stop icon to match the one in spotify's UI
* implement analysis view
* use authorization code flow instead of implicit grant, so that sessions last longer
* export playlist
* think of a better name + logo/favicon
* landing page w/ screenshots (with good SEO practices)
* mobile responsiveness

## Nice-to-haves
* persist in-progress playlists remotely (i.e. in s3, on a per-spotify-user basis)
* navigate through search results with up/down arrow

