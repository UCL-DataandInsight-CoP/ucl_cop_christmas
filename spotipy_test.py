import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
import json
from bs4 import BeautifulSoup

def request_song_info(song_title, artist_name):
    base_url = 'https://api.genius.com'
    headers = {'Authorization': 'Bearer ' + 'XfY0zl7MRjxuzVzMK9Z9tJy7ddLF64wgSIC2SUMcKdlQ4wMWUkkTEFkrr2iAMfFN'}
    search_url = base_url + '/search'
    data = {'q': song_title + ' ' + artist_name}
    response = requests.get(search_url, data=data, headers=headers)

    return response

def request_song_info(song_title, artist_name):
    base_url = 'https://api.genius.com'
    headers = {'Authorization': 'Bearer ' + 'XfY0zl7MRjxuzVzMK9Z9tJy7ddLF64wgSIC2SUMcKdlQ4wMWUkkTEFkrr2iAMfFN'}
    search_url = base_url + '/search'
    data = {'q': song_title + ' ' + artist_name}
    response = requests.get(search_url, data=data, headers=headers)

    return response

def scrap_song_url(url):
    page = requests.get(url)
    html = BeautifulSoup(page.text, 'html.parser')
    [h.extract() for h in html('script')]
    lyrics = html.find('div', class_='lyrics').get_text()

    return lyrics

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

    response = request_song_info(title, artist)
    json = response.json()
    remote_song_info = None

    for hit in json['response']['hits']:
        if artist.lower() in hit['result']['primary_artist']['name'].lower():
            remote_song_info = hit
            break
    if remote_song_info:
        song_url = remote_song_info['result']['url']
        lyrics = scrap_song_url(song_url)

    print(title + ', ' + artist + ', ' + song_link + ', ' + str(features), lyrics)










