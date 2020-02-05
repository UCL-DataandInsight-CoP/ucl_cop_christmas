## UCL Community of Practice: Christmas Songs

### UCL Community of Practice Christmas Meetup Data Competition

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
```


<img src="dataframe.PNG?raw=true"/>

#### Scraping Song Lyrics, Genius.com

Genius is a website/API containing lyrics for a wide variety of songs. Once the playlist
tracks were searched and stored from Spotify, the Genius API was used to find matches
and BeautifulSoup was used to scrape the lyrics from the matches Genius webpages.

The following function allows a song title and artist to be passed in, here using
the results from Spotify, and to return a match to the Genius.com webpage containing
the lyrics for that song:

```python
'''
genius_song_details

get song details through search of genius api

title: String, song title
artist: String, artist name

returns API RESPONSE
'''
def genius_song_details(title, artist):
    genius_api = 'https://api.genius.com'
    headers = {'Authorization': 'Bearer ' + ''}
    genius_search = genius_api + '/search'
    data = {'q': title + ' ' + artist}
    response = requests.get(genius_search, data=data, headers=headers)

    return response
```

Once a matching webpage has been found, the following function uses
BeautifulSoup to scrape the lyrics by exploting the common structure
of Genius.com lyrics webpages:

```python
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
```

These were utilised to source and add the lyrics for each song
to the DataFrames:

```python
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

lyrics.append(song_lyrics.replace(',', '')) # append lyrics, remove commas to avoid csv conflicts
```

<img src="lyrics.PNG?raw=true"/>

#### Extracting the Data

For each Playlist DataFrame, the results were outputted to csv files:

```python
'''
For each DataFrame, representing a playlist, export as individual csv file
'''
track_dataframe.to_csv(str(playlist_name) + '.csv', index=False)
```

and once all csv files are exported, a combined csv file of all the song data
collected is produced by looping through each file and concatonating 
into a new Pandas DataFrame for export:

```python
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
```

In addition, all of the contents of the lyrics were written to a seperate text file
to create a corpus of all of the words used in Christmas songs, to be used to
create a word cloud visualisation in the next stage:

```python
'''
write lyrics to text file
'''
christmas_lyrics = open("christmas_lyrics.txt","a+")
if song_lyrics != 'NO MATCH':
    christmas_lyrics.write(str(song_lyrics) + "\n")
```

### Data Visualisation

#### Christmas Lyrics Wordcloud

For the visualisation, I used the collection of christmas lyrics
to create a wordcloud of the most commonly used words.

```python
text = " ".join(lyrics for lyrics in df.lyrics)
print ("{} total words in lyrics.".format(len(text)))

1811704 total words in lyrics.
```

Common english stopwords (the, I, and etc.....) were removed to prevent them from domintating
the most used words:

```python
stopwords = set(STOPWORDS)
```

```python
Initially, I created a basic wordcloud of the top 1000 christmas lyrics used:


# Create a word cloud image
wc = WordCloud(background_color="black", max_words=1000, mask=transformed_tree_mask,
               stopwords=stopwords, contour_width=3, contour_color='firebrick')

# Generate a wordcloud
wc.generate(text)

# store to file
#wc.to_file("img/wine.png")

# show
plt.figure(figsize=[20,10])
plt.imshow(wc, interpolation='bilinear')
plt.axis("off")
plt.show()
```

<img src="basic_wordcloud.PNG?raw=true"/>

Following this, taking inspiration from a wordcloud shaped and colored as [Alice in Wonderland](https://raw.githubusercontent.com/fuqiuai/wordCloud/master/Images/alice.png) from the WordCloud python library documentation, I used a simple vector image of a Christmas Tree:

<img src="tree.png?raw=true"/>

to create a shape and colour mask to
fit a custom Christmas Song Lyric Tree WordCloud visualisation:

<img src="word_cloud.png?raw=true"/>