## UCL Community of Practice: Christmas Songs

### Outline

Source christmas songs and lyrics data from the Spotify and Genius APIs using Python. Create an
interesting visualisation. 

### Data Collection Pipeline

The data colelction pipeline for this project collects song information from all official
Spotify Christmas playlists using the Spotify API and then scraped the associated song lyrics
from Genius.com

CSVs are crated for each playlist and a combined file of all the songs created. The lyrics are also
stored seperately as text only for later analysis and visualisation.

#### Collecting Spotify Christmas Songs

A connection to the Spotify API was establised using the Spotipy python library with authentication
keys generated from the Spotify developer's portal:

```python
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

cid = ''
secret = ''
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
```

The cid and secret variables can be replaced with a user's own keys.

Using the API connection, Christmas playlists were identified by searching the Spotify
JSON data for playlsuts created by Spotify themselves and contain the word 'Christmas':

```python
'''
search the Spotify API for playlists mentioning 'christmas'
for each match, if the playlist is Spotify curated, collect and store the ID
'''
christmas_playlists = sp.search(q='christmas', type='playlist')
playlists = [] # 
for playlist in christmas_playlists['playlists']['items']:
    id = playlist['id']
    user = playlist['owner']['id']
    if user == 'spotify':
        playlists.append(id)
```

Then for each playlist collected in the search, the following information
was extracted for each playlist and song:

* Playlist Tile
* Artist Name
* Track Name
* Song URL
* Danceability
* Energy
* Loudness
* Valence
* Tempo

Each feature was stored in seperate arrays and then transofmred into
readable Pandas DataFrames represeting the tracklists and song info
for each playlist:

```python
for playlist_id in playlists:
    results = sp.user_playlist('spotify', str(playlist_id))
    playlist_name = results['name']
    print('Processing - ' + playlist_name)


    playlist_title = []
    artist_name = []
    track_name = []
    url = []
    danceability = []
    energy = []
    loudness = []
    valence = []
    temp = []
    lyrics = []

    '''
    for each song listed in each playist
    extract the details and store in arrays
    arrays will be used as Pandas Series' for final DataFrame construction
    '''
    for song in results['tracks']['items']:
        if results['tracks']['items'] is not None:
            playlist_title = playlist_name
            title = song['track']['name']
            artist = song['track']['artists'][0]['name']
            song_id = song['track']['id']
            song_link = 'https://open.spotify.com/track/'+str(song_id)
            song_danceability = sp.audio_features(song_id)[0]['danceability']
            song_energy = sp.audio_features(song_id)[0]['energy']
            song_loudness = sp.audio_features(song_id)[0]['loudness']
            song_valence = sp.audio_features(song_id)[0]['valence']
            song_temp = sp.audio_features(song_id)[0]['tempo']
```

<img src="dataframe.png?raw=true"/>