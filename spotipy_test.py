import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

cid = '0786700255834c229778011930c57d24'
secret = 'd9565e37c7584e9fab41e95df0ffa3c5'

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

#results = sp.search(q='offspring:', type='artist')
username = 'Spotify'
playlist_id = '37i9dQZF1DX0Yxoavh5qJV'
results = sp.user_playlist(username, playlist_id)
#print(results)
for song in results['tracks']['items']:
    title = song['track']['name']
    artist = song['track']['artists'][0]['name']
    song_id = song['track']['id']
    song_link = 'https://open.spotify.com/track/'+str(song_id)
    song_danceability = sp.audio_features(song_id)[0]['danceability']
    song_energy = sp.audio_features(song_id)[0]['energy']
    song_loudness = sp.audio_features(song_id)[0]['loudness']
    song_valence = sp.audio_features(song_id)[0]['valence']
    song_temp = sp.audio_features(song_id)[0]['tempo']
    features = [song_danceability, song_energy, song_loudness, song_temp, song_valence]
    print(title + ', ' + artist + ', ' + song_link + ', ' + str(features))