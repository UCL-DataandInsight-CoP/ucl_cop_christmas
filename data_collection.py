'''
Christmas Songs - UCL Data and Insight Community of Practice

Source song details and lyrics for Christmas Songs
curated on Spotify offical playlists

Lyrics scraped from Genius.com

Sam McIlroy
'''

#setup and helper functions
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
import os
import glob

'''
genius_song_details

get song details through search of genius api

title: String, song title
artist: String, artist name

returns API RESPONSE
'''
def genius_song_details(title, artist):
    genius_api = 'https://api.genius.com'
    headers = {'Authorization': 'Bearer ' + 'XfY0zl7MRjxuzVzMK9Z9tJy7ddLF64wgSIC2SUMcKdlQ4wMWUkkTEFkrr2iAMfFN'}
    genius_search = genius_api + '/search'
    data = {'q': title + ' ' + artist}
    response = requests.get(genius_search, data=data, headers=headers)

    return response

'''
scrape_lyrics

Use the Beautiful Soup library to scrape Genius.com lyrics pages
Exploits html/structure tags

url: genius API url

returns: lyrics, HTML formatting
'''
def scrape_lyrics(url):
    link = requests.get(url)
    html = BeautifulSoup(link.text, 'html.parser')
    [elem.extract() for elem in html('script')]
    lyrics = html.find('div', class_='lyrics').get_text()

    return lyrics

'''
main

retrieve song details for each Spotify playlist
scrape lyrics from Genius
output to csv for further analysis
'''
def main():

    # manage API credentials for Spotify and Genius
    cid = ''
    secret = ''
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

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

    '''
    for each playlist found, collect details from the Spotify API

    Playlist Tile
    Artist Name
    Track Name
    Song URL
    Danceability
    Energy
    Loudness
    Valence
    Tempo
    '''
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

            '''
            collect lyrics matches from Genius...
            '''
            genius_api_response = genius_song_details(title, artist)
            json = genius_api_response.json()
            remote_song_info = None
            '''
            for each song in the playist
            retrieve the song title and artist name and pass to Genius API scraper function
            if there is a match, scrape/retrieve the lyrics
            if not record NO MATCH
            '''
            for hit in json['response']['hits']:
                if artist.lower() in hit['result']['primary_artist']['name'].lower():
                    remote_song_info = hit
                    break
            if remote_song_info:
                song_url = remote_song_info['result']['url']
                song_lyrics = scrape_lyrics(song_url)
            else:
                song_lyrics = 'NO MATCH'

            '''
            append to arrays
            '''
            print('Appending: ' + artist + ', ' + title)
            artist_name.append(artist)
            track_name.append(title)
            url.append(song_link)
            danceability.append(song_danceability)
            energy.append(song_energy)
            loudness.append(song_loudness)
            valence.append(song_valence)
            temp.append(song_temp)
            lyrics.append(song_lyrics.replace(',', '')) # append lyrics, remove commas to avoid csv conflicts

            '''
            write lyrics to text file
            '''
            christmas_lyrics = open("christmas_lyrics.txt","a+")
            if song_lyrics != 'NO MATCH':
                christmas_lyrics.write(str(song_lyrics) + "\n")

        '''
        build Pandas dataframe from collected arrays/Series'
        '''
        track_dataframe = pd.DataFrame({'playlist_name' : playlist_title,
                                        'artist_name' : artist_name,
                                        'track_name' : track_name,
                                        'url' : url,
                                        'danceability' : danceability,
                                        'energy': energy,
                                        'loudness': loudness,
                                        'valence': valence,
                                        'tempo': temp,
                                        'lyrics': lyrics})
        '''
        tidy for output

        remove non-matches, tracks where details from Genius API could not be found
        '''
        track_dataframe = track_dataframe[track_dataframe['lyrics'] != 'NO MATCH']
  

        print(track_dataframe) # print output to console....

        '''
        For each DataFrame, representing a playlist, export as individual csv file
        '''
        track_dataframe.to_csv(str(playlist_name) + '.csv', index=False)

            

    

    '''
    once all playlists have been processed, each will have a .csv file populated

    for all .csv files created, append together to create a combined, final output of
    all playlists
    '''
    extension = 'csv'
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

    '''
    concat the playlist csv' and export as combined dataset
    '''
    #combine all files in the list
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
    #export to csv
    combined_csv.to_csv( "All Playlists Combined.csv", index=False, encoding='utf-8-sig')

'''
Run the processing

Collect the relevant playlist IDs
Process each track for data from the Spotify API
Check for matches with the Genius API
Scrape lyrics from relevane Genius webpages
Export details and lyrics as csv, exclude non-matches
Combine all playlists into a single dataset, to be shared for analysis
'''
if __name__ == '__main__':
    main()




